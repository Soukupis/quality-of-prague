"""Park and Ride (P+R) capacity and intermodality section."""
from dash import html
import dash_bootstrap_components as dbc
from src.components.ui import section_header
from src.utils.geospatial_utils import points_within_polygon
from src.utils.loaders.districts_loader import get_parking_p_r_data
from src.components.config import theme
from src.i18n import t

_STAV_KEYS = {1: "pr_stav_operating", 4: "pr_stav_planned", 5: "pr_stav_operating"}


def _get_pr_stats(district_polygon, lang="cs"):
    data = get_parking_p_r_data()
    within = points_within_polygon(district_polygon, data, "geometry")

    if len(within) == 0:
        return None

    current_capacity = int(within["kapacita"].fillna(0).sum())
    planned_mask = within["kapacita_vyhled"].notna() & (within["kapacita_vyhled"] > 0)
    planned_capacity = int(within.loc[planned_mask, "kapacita_vyhled"].sum())

    facilities = []
    for _, row in within.iterrows():
        name = row.get("nazev", "—")
        cap = int(row["kapacita"]) if not (hasattr(row["kapacita"], "__float__") and
                                            row["kapacita"] != row["kapacita"]) else 0
        planned = int(row["kapacita_vyhled"]) if (
            row.get("kapacita_vyhled") and row["kapacita_vyhled"] == row["kapacita_vyhled"]
        ) else None
        stav_key = _STAV_KEYS.get(int(row.get("stav", 1)), "pr_stav_operating")
        stav = t(stav_key, lang)
        facilities.append({"name": name, "capacity": cap, "planned": planned, "stav": stav})

    return {
        "count": len(within),
        "current_capacity": current_capacity,
        "planned_capacity": planned_capacity,
        "facilities": facilities,
    }


def _facility_row(facility, lang):
    planned_badge = html.Span(
        t("pr_planned_badge", lang, planned=facility["planned"]),
        style={"fontSize": "0.75rem", "color": "#059669",
               "fontWeight": "600", "marginLeft": "0.4rem"}
    ) if facility["planned"] else None

    return html.Tr([
        html.Td(facility["name"],
                style={"fontSize": "0.85rem", "fontWeight": "500",
                       "color": "#1e293b", "paddingRight": "1rem"}),
        html.Td([
            html.Span(t("pr_spaces_unit", lang, cap=facility["capacity"]),
                      style={"fontSize": "0.85rem", "color": "#475569"}),
            planned_badge,
        ], style={"whiteSpace": "nowrap"}),
        html.Td(
            html.Span(facility["stav"],
                      style={"fontSize": "0.75rem", "background": "#dcfce7", "color": "#15803d",
                             "borderRadius": "8px", "padding": "2px 8px", "fontWeight": "600"}),
        ),
    ], style={"borderBottom": "1px solid #f1f5f9"})


def pr_section(district, polygons, lang="cs"):
    if district not in polygons:
        return None

    stats = _get_pr_stats(polygons[district], lang)
    if stats is None:
        return None

    def _stat_card(icon_class, label, value, color="#0f766e", bg="linear-gradient(135deg, #f0fdfa 0%, #ffffff 100%)"):
        return dbc.Card(
            dbc.CardBody(html.Div([
                html.I(className=f"fa-solid {icon_class}",
                       style={"fontSize": "1.3rem", "color": color, "minWidth": "1.6rem"}),
                html.Div([
                    html.Div(label, style={"fontSize": "0.8rem", "color": "#64748b", "fontWeight": "500"}),
                    html.Div(str(value), style={"fontSize": "1.3rem", "fontWeight": "700", "color": "#1e293b"}),
                ], style={"marginLeft": "0.5rem"})
            ], className="d-flex align-items-center")),
            className="shadow-sm h-100",
            style={"border": "none", "borderRadius": "0.75rem", "background": bg},
        )

    summary_cards_list = [
        dbc.Col(_stat_card("fa-car-side", t("pr_pr_count", lang), stats["count"]),
                xs=6, sm=4, md=3, className="mb-3"),
        dbc.Col(_stat_card("fa-square-parking", t("pr_capacity", lang),
                            t("pr_spaces_unit", lang, cap=stats["current_capacity"])),
                xs=6, sm=4, md=3, className="mb-3"),
    ]
    if stats["planned_capacity"] > 0:
        summary_cards_list.append(
            dbc.Col(_stat_card("fa-chart-line", t("pr_planned", lang),
                               t("pr_spaces_unit", lang, cap=stats["planned_capacity"]),
                               color="#059669",
                               bg="linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%)"),
                    xs=6, sm=4, md=3, className="mb-3")
        )

    summary_cards = dbc.Row(summary_cards_list, className="g-2 mb-3")

    facility_table = html.Div([
        html.H6(t("pr_table_title", lang),
                style={"color": "#134e4a", "fontWeight": "600",
                       "fontSize": "0.9rem", "marginBottom": "0.5rem"}),
        html.Table(
            [html.Tbody([_facility_row(f, lang) for f in stats["facilities"]])],
            style={"width": "100%", "borderCollapse": "collapse"}
        )
    ], style={"background": "#f8fafc", "borderRadius": "0.75rem", "padding": "0.75rem 1rem",
              "marginBottom": "0.5rem"})

    return dbc.Row([
        dbc.Col([
            section_header(
                title=t("section_pr", lang),
                accent_color=theme.TRAVEL_ACCENT_COLOR,
                bg_color=theme.TRAVEL_BG_COLOR,
                text_color=theme.TRAVEL_TEXT_COLOR,
            ),
            summary_cards,
            facility_table,
        ], width=12)
    ])
