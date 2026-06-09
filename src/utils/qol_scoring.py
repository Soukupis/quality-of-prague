"""Shared QoL composite scoring engine.

Computes QOUL domain scores (0–100) and the composite QoL index for every
Prague district using min-max normalization — the OECD Better Life Index method.

Domain weights:
    Bezpečnost    30% — police station density / km²
    Mobilita      37% — metro density (70%) + elevator ratio (30%)
    Přístupnost   23% — ZTP density (60%) + elevator ratio (40%)
    Prostředí     10% — park density (OSM leisure=park per km²)

This module is the single source of truth for scoring so that qol_index.py
and dashboard.py share the same computation and cache.
"""
from src.utils.districts.district_utils import (
    get_district_polygons, get_district_areas_km2, get_points_in_district
)
from src.components.pages.district_info.accessibility_section import (
    _get_metro_accessibility_stats, _get_ztp_stats
)
from src.utils.geospatial_utils import points_within_polygon
from src.utils.loaders.districts_loader import get_parks_data

DOMAIN_LABELS = ["Bezpečnost", "Mobilita", "Přístupnost", "Prostředí"]
DOMAIN_LABEL_KEYS = [
    "domain_label_safety",
    "domain_label_mobility",
    "domain_label_accessibility",
    "domain_label_environment",
]
DOMAIN_COLORS = ["#0f766e", "#1d4ed8", "#7c3aed", "#16a34a"]
DOMAIN_ICONS = ["fa-shield-halved", "fa-train-subway", "fa-wheelchair", "fa-tree"]
DOMAIN_WEIGHTS = [0.30, 0.37, 0.23, 0.10]


def compute_raw_scores():
    polygons = get_district_polygons()
    areas = get_district_areas_km2()
    parks_data = get_parks_data()
    raw = {}

    for district, polygon in polygons.items():
        area = areas.get(district, 1.0)
        police_count = len(get_points_in_district(district, "police_stations"))
        metro_count = len(get_points_in_district(district, "subway_entrances"))
        metro_stats = _get_metro_accessibility_stats(polygon)
        ztp_stats = _get_ztp_stats(district, polygon)
        park_count = len(points_within_polygon(polygon, parks_data, "geometry"))

        raw[district] = {
            "police_density": police_count / area,
            "metro_density": metro_count / area,
            "elevator_ratio": metro_stats["lift_ratio"],
            "ztp_density": ztp_stats["total_spaces"] / area,
            "park_density": park_count / area,
        }

    return raw


def _normalize_min_max(raw, key):
    """Normalize one indicator to 0–100 via min-max scaling."""
    values = [v[key] for v in raw.values()]
    min_v, max_v = min(values), max(values)
    if max_v == min_v:
        return {d: 50.0 for d in raw}
    return {d: round((raw[d][key] - min_v) / (max_v - min_v) * 100, 1) for d in raw}


def compute_domain_scores(raw):
    police_norm = _normalize_min_max(raw, "police_density")
    metro_norm = _normalize_min_max(raw, "metro_density")
    elevator_norm = _normalize_min_max(raw, "elevator_ratio")
    ztp_norm = _normalize_min_max(raw, "ztp_density")
    park_norm = _normalize_min_max(raw, "park_density")

    scores = {}
    for d in raw:
        safety = police_norm[d]
        mobility = round(metro_norm[d] * 0.7 + elevator_norm[d] * 0.3, 1)
        accessibility = round(ztp_norm[d] * 0.6 + elevator_norm[d] * 0.4, 1)
        environment = park_norm[d]
        scores[d] = [safety, mobility, accessibility, environment]

    return scores


def composite_score(domain_scores):
    """Weighted composite — Safety 30%, Mobility 37%, Accessibility 23%, Environment 10%."""
    s, m, a, e = domain_scores
    return round(s * 0.30 + m * 0.37 + a * 0.23 + e * 0.10, 1)


_cached_scores = None


def get_all_scores():
    """Return domain scores for all districts, computed once and cached."""
    global _cached_scores
    if _cached_scores is None:
        raw = compute_raw_scores()
        _cached_scores = compute_domain_scores(raw)
    return _cached_scores
