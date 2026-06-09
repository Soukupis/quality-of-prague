"""Environmental health section for district detail pages.

Operationalises the QOUL Environmental Health domain by showing:
  - Green space (parks) count and density in the district
  - Nearest ČHMÚ air quality monitoring station and its type

Theory reference: QOUL Environmental Health — green space access, PM2.5/PM10/NO₂
exposure; WHOQOL Physical domain (outdoor recreation); 15-Minute City 'Fun'
social function; urban heat island vulnerability (Jan persona, age 75, Praha 7).
"""
from typing import Optional

from dash import html
import dash_bootstrap_components as dbc
from shapely.geometry import Point

from src.components.ui import section_header
from src.components.config import theme
from src.utils.geospatial_utils import points_within_polygon
from src.utils.loaders.districts_loader import get_parks_data, get_chmi_stations_data
from src.utils.districts.district_utils import get_district_areas_km2


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
    """Find nearest ČHMÚ monitoring station to the district centroid."""
    stations = get_chmi_stations_data()
    if stations.empty:
        return None

    # Project to EPSG:5514 for accurate distance in metres
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

    # Check if station is within the district
    within = points_within_polygon(district_polygon, stations, "geometry")
    in_district = len(within) > 0
    in_district_name = nearest["name"] if in_district else None

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


def environment_section(district: str, polygons: dict):
    """Create the environmental health section for a district detail page.

    Shows park count/density and the nearest ČHMÚ air quality monitoring station.

    Args:
        district: District name (e.g., "Praha 7").
        polygons: Dict mapping district names to Shapely polygon geometries.

    Returns:
        dbc.Row with the environment section, or None if no data available.
    """
    if district not in polygons:
        return None

    polygon = polygons[district]
    park_stats = _get_park_stats(district, polygon)
    chmi = _get_nearest_chmi(polygon)

    # --- Parks subsection ---
    parks_content = [
        html.H6("Parky a zeleň",
                style={"color": theme.ENVIRONMENT_TEXT_COLOR, "fontWeight": "600",
                       "fontSize": "0.9rem", "marginBottom": "0.5rem"}),
        dbc.Row([
            dbc.Col(_env_stat_card("fa-tree", "Parků celkem", park_stats["count"], "#16a34a"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_env_stat_card("fa-tag", "Pojmenovaných", park_stats["named"], "#15803d"),
                    xs=6, sm=4, md=3, className="mb-3"),
            dbc.Col(_env_stat_card("fa-map", "Parků / km²", f"{park_stats['density']:.2f}", "#166534"),
                    xs=6, sm=4, md=3, className="mb-3"),
        ], className="g-2 mb-2"),
        dbc.Alert([
            html.I(className="fa-solid fa-circle-info me-2", style={"color": "#16a34a"}),
            html.Span("Data z OpenStreetMap (leisure=park). Zahrnuje pojmenované i nepojmenované "
                      "zelené plochy v administrativních hranicích obvodu.",
                      style={"fontSize": "0.8rem", "color": "#374151"})
        ], color="success",
           style={"padding": "0.5rem 0.75rem", "borderRadius": "0.5rem",
                  "background": "#f0fdf4", "border": "1px solid #bbf7d0",
                  "marginBottom": "0.75rem", "fontSize": "0.8rem"}),
    ]

    # --- ČHMÚ nearest station subsection ---
    chmi_content = []
    if chmi:
        station_in_badge = html.Span(
            "v obvodu" if chmi["in_district"] else f"{chmi['distance_km']} km",
            style={
                "display": "inline-block",
                "background": "#16a34a" if chmi["in_district"] else "#d97706",
                "color": "white",
                "borderRadius": "12px",
                "padding": "2px 10px",
                "fontSize": "0.82rem",
                "fontWeight": "600",
                "marginLeft": "0.5rem",
                "verticalAlign": "middle",
            }
        )

        type_label = {
            "pozaďová": "Pozaďová — měří obecné znečištění oblasti",
            "dopravní": "Dopravní — měří znečištění z automobilového provozu",
            "průmyslová": "Průmyslová — měří znečištění z průmyslových zdrojů",
        }.get(chmi.get("station_type", ""), chmi.get("station_type", "—"))

        chmi_content = [
            html.H6("Kvalita ovzduší — nejbližší monitorovací stanice",
                    style={"color": theme.ENVIRONMENT_TEXT_COLOR, "fontWeight": "600",
                           "fontSize": "0.9rem", "marginBottom": "0.5rem", "marginTop": "0.75rem"}),
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fa-solid fa-wind me-2",
                               style={"color": "#16a34a", "fontSize": "1.1rem"}),
                        html.Span(chmi["name"],
                                  style={"fontWeight": "700", "fontSize": "0.95rem",
                                         "color": "#1e293b"}),
                        station_in_badge,
                    ], className="d-flex align-items-center mb-2"),
                    html.Div([
                        html.Span("Kód: ", style={"fontSize": "0.82rem", "color": "#64748b"}),
                        html.Span(chmi["code"],
                                  style={"fontSize": "0.82rem", "fontWeight": "600",
                                         "color": "#334155", "marginRight": "1rem"}),
                        html.Span("Typ: ", style={"fontSize": "0.82rem", "color": "#64748b"}),
                        html.Span(type_label,
                                  style={"fontSize": "0.82rem", "color": "#334155"}),
                    ], className="mb-1"),
                    html.Div(
                        "Data o měřeních (PM2.5, PM10, NO₂, O₃) jsou dostupná přes API "
                        f"ČHMÚ pro stanici {chmi['code']}. Integraci naměřených hodnot "
                        "plánujeme v další fázi (Phase 4).",
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
                title="Životní prostředí",
                accent_color=theme.ENVIRONMENT_ACCENT_COLOR,
                bg_color=theme.ENVIRONMENT_BG_COLOR,
                text_color=theme.ENVIRONMENT_TEXT_COLOR,
            ),
            *parks_content,
            *chmi_content,
        ], width=12)
    ])
