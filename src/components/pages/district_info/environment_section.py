"""Environmental health section for district detail pages."""
from typing import Optional

from dash import html
import dash_bootstrap_components as dbc
from shapely.geometry import Point

from src.components.ui import section_header
from src.components.config import theme
from src.utils.geospatial_utils import points_within_polygon
from src.utils.loaders.districts_loader import get_parks_data, get_chmi_stations_data
from src.utils.districts.district_utils import get_district_areas_km2
from src.i18n import t


_STATION_TYPE_KEYS = {
    "pozaďová":  "env_station_background",
    "dopravní":  "env_station_traffic",
    "průmyslová": "env_station_industrial",
}


def _get_park_stats(district: str, district_polygon) -> dict:
    parks = get_parks_data()
    within = points_within_polygon(district_polygon, parks, "geometry")
    count = len(within)
    named = int(within["name"].notna().sum()) if count > 0 else 0
    areas = get_district_areas_km2()
    area_km2 = areas.get(district, 1.0)
    density = round(count / area_km2, 2) if area_km2 > 0 else 0.0
    return {"count": count, "named": named, "density": density, "area_km2": area_km2}


def _get_nearest_chmi(district_polygon) -> Optional[dict]:
    stations = get_chmi_stations_data()
    if stations.empty:
        return None

    centroid = district_polygon.centroid
    centroid_pt = Point(centroid.x, centroid.y)

    import geopandas as gpd
    stations_proj = stations.to_crs(5514)
    centroid_gdf = gpd.GeoDataFrame(
        geometry=[centroid_pt], crs="EPSG:4326"
    ).to_crs(5514)
    centroid_proj = centroid_gdf.geometry.iloc[0]

    distances = stations_proj.geometry.distance(centroid_proj)
    idx = distances.idxmin()
    nearest = stations.loc[idx]
    dist_km = round(distances[idx] / 1000, 1)

    within = points_within_polygon(district_polygon, stations, "geometry")
    in_district = len(within) > 0

    return {
        "name": nearest["name"],
        "code": nearest["station_code"],
        "station_type": nearest.get("station_type", ""),
        "zone_type": nearest.get("zone_type", ""),
        "distance_km": dist_km,
        "in_district": in_district,
    }


def _env_stat_card(icon_class, label, value, color="#14532d"):
    return dbc.Card(
        dbc.CardBody(
            html.Div([
                html.I(className=f"fa-solid {icon_class}",
                       style={"fontSize": "1.3rem", "color": color, "minWidth": "1.6rem"}),
                html.Div([
                    html.Div(label, style={"fontSize": "0.8rem", "color": "#64748b",
                                           "fontWeight": "500", "lineHeight": "1.2"}),
                    html.Div(str(value), style={"fontSize": "1.3rem", "fontWeight": "700",
                                                "color": "#1e293b", "lineHeight": "1.3"}),
                ], style={"marginLeft": "0.5rem"})
            ], className="d-flex align-items-center"),
        ),
        className="shadow-sm h-100",
        style={"border": "none", "borderRadius": "0.75rem",
               "background": "linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%)"}
    )


def environment_section(district: str, polygons: dict, lang: str = "cs"):
    if district not in polygons:
        return None

    polygon = polygons[district]
    park_stats = _get_park_stats(district, polygon)
    chmi = _get_nearest_chmi(polygon)

    parks_content = [
        html.H6(t("env_parks_header", lang),
                style={"color": theme.ENVIRONMENT_TEXT_COLOR, "fontWeight": "600",
                       "fontSize": "0.9rem", "marginBottom": "0.5rem"}),
        dbc.Row([
            dbc.Col(_env_stat_card("fa-tree", t("env_parks_total", lang),
                                   park_stats["count"], "#16a34a"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_env_stat_card("fa-tag", t("env_parks_named", lang),
                                   park_stats["named"], "#15803d"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_env_stat_card("fa-map", t("env_parks_density", lang),
                                   f"{park_stats['density']:.2f}", "#166534"),
                    xs=6, sm=4, md=3, className="mb-3"),
        ], className="g-2 mb-2"),
        dbc.Alert([
            html.I(className="fa-solid fa-circle-info me-2", style={"color": "#16a34a"}),
            html.Span(t("env_parks_note", lang),
                      style={"fontSize": "0.8rem", "color": "#374151"})
        ], color="success",
           style={"padding": "0.5rem 0.75rem", "borderRadius": "0.5rem",
                  "background": "#f0fdf4", "border": "1px solid #bbf7d0",
                  "marginBottom": "0.75rem", "fontSize": "0.8rem"}),
    ]

    chmi_content = []
    if chmi:
        station_in_badge = html.Span(
            t("env_chmi_in_district", lang) if chmi["in_district"] else f"{chmi['distance_km']} km",
            style={
                "display": "inline-block",
                "background": "#16a34a" if chmi["in_district"] else "#d97706",
                "color": "white", "borderRadius": "12px", "padding": "2px 10px",
                "fontSize": "0.82rem", "fontWeight": "600",
                "marginLeft": "0.5rem", "verticalAlign": "middle",
            }
        )

        type_key = _STATION_TYPE_KEYS.get(chmi.get("station_type", ""))
        type_label = t(type_key, lang) if type_key else (chmi.get("station_type") or "—")

        chmi_content = [
            html.H6(t("env_chmi_header", lang),
                    style={"color": theme.ENVIRONMENT_TEXT_COLOR, "fontWeight": "600",
                           "fontSize": "0.9rem", "marginBottom": "0.5rem", "marginTop": "0.75rem"}),
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fa-solid fa-wind me-2",
                               style={"color": "#16a34a", "fontSize": "1.1rem"}),
                        html.Span(chmi["name"],
                                  style={"fontWeight": "700", "fontSize": "0.95rem", "color": "#1e293b"}),
                        station_in_badge,
                    ], className="d-flex align-items-center mb-2"),
                    html.Div([
                        html.Span(t("env_chmi_code", lang),
                                  style={"fontSize": "0.82rem", "color": "#64748b"}),
                        html.Span(chmi["code"],
                                  style={"fontSize": "0.82rem", "fontWeight": "600",
                                         "color": "#334155", "marginRight": "1rem"}),
                        html.Span(t("env_chmi_type", lang),
                                  style={"fontSize": "0.82rem", "color": "#64748b"}),
                        html.Span(type_label, style={"fontSize": "0.82rem", "color": "#334155"}),
                    ], className="mb-1"),
                    html.Div(
                        t("env_chmi_future_note", lang, code=chmi["code"]),
                        style={"fontSize": "0.78rem", "color": "#94a3b8", "marginTop": "0.25rem"}
                    ),
                ])
            ], className="shadow-sm",
               style={"border": "1px solid #bbf7d0", "borderRadius": "0.75rem",
                      "background": "#f8fffe", "marginBottom": "0.5rem"}),
        ]

    if park_stats["count"] == 0 and not chmi_content:
        return None

    return dbc.Row([
        dbc.Col([
            section_header(
                title=t("section_environment", lang),
                accent_color=theme.ENVIRONMENT_ACCENT_COLOR,
                bg_color=theme.ENVIRONMENT_BG_COLOR,
                text_color=theme.ENVIRONMENT_TEXT_COLOR,
            ),
            *parks_content,
            *chmi_content,
        ], width=12)
    ])
