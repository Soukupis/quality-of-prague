import dash_bootstrap_components as dbc
from dash import html

from ..ui import icon, nav_item
from ..config import SIDEBAR_STYLE, NAV_ITEMS, TEXT_COLOR, FONT_WEIGHT_BOLD, FONT_SIZE_LARGE, SPACING_XL
from src.i18n import t

_NAV_LABEL_KEYS = {
    "Domů":          "nav_home",
    "Městské části": "nav_districts",
    "Dashboard":     "nav_dashboard",
    "QoL Index":     "nav_qol_index",
    "Teorie":        "nav_theory",
    "Persony":       "nav_personas",
    "Datové sady":   "nav_datasets",
    "O Aplikaci":    "nav_about",
    "Analýza dat":   "nav_group_analysis",
    "Metodologie":   "nav_group_methodology",
    "Zdroje":        "nav_group_sources",
}


def _render_nav_items(lang: str = "cs"):
    """Build nav item list with translated labels and lang-aware hrefs."""
    items = []
    for item in NAV_ITEMS:
        label_key = _NAV_LABEL_KEYS.get(item.get("label", ""))
        label = t(label_key, lang) if label_key else item.get("label", "")

        if item.get("type") == "divider":
            items.append(html.Div(
                label,
                style={
                    "fontSize": "0.7rem",
                    "color": "#94a3b8",
                    "fontWeight": "700",
                    "letterSpacing": "0.08em",
                    "textTransform": "uppercase",
                    "padding": "0.75rem 1.5rem 0.25rem",
                }
            ))
        else:
            href = item["href"]
            if lang and lang != "cs":
                href = f"{href}?lang={lang}"
            items.append(nav_item(
                label=label,
                href=href,
                icon_name=item["icon"],
                variant="sidebar"
            ))
    return items


def _lang_switcher(lang: str = "cs"):
    def _btn(code, active):
        return html.Button(
            code.upper(),
            id=f"btn-lang-{code}",
            n_clicks=0,
            style={
                "background": "#667eea" if active else "transparent",
                "color": "white" if active else "#94a3b8",
                "border": "1px solid #667eea" if active else "1px solid #cbd5e1",
                "borderRadius": "0.35rem",
                "padding": "3px 10px",
                "fontSize": "0.78rem",
                "fontWeight": "700",
                "cursor": "pointer",
                "marginRight": "0.25rem",
                "transition": "all 0.15s",
            }
        )

    return html.Div([
        html.Div(
            t("lang_label", lang),
            style={"fontSize": "0.65rem", "color": "#94a3b8", "fontWeight": "700",
                   "letterSpacing": "0.08em", "textTransform": "uppercase",
                   "marginBottom": "0.35rem"}
        ),
        html.Div([_btn("cs", lang == "cs"), _btn("en", lang == "en")], className="d-flex"),
    ], style={"padding": "0.75rem 1.5rem", "marginTop": "0.5rem",
              "borderTop": "1px solid rgba(0,0,0,0.07)"})


def sidebar_header(lang: str = "cs"):
    return html.Div([
        html.H3([
            icon(name="list", class_name="me-2"),
            t("nav_navigation", lang),
        ], className="mb-0", style={
            "color": TEXT_COLOR,
            "fontWeight": FONT_WEIGHT_BOLD,
            "fontSize": FONT_SIZE_LARGE,
        }),
    ], style={"padding": f"0 {SPACING_XL}", "marginBottom": SPACING_XL})


def sidebar(lang: str = "cs"):
    return html.Div([
        sidebar_header(lang),
        dbc.Nav(
            id="sidebar-nav-container",
            children=_render_nav_items(lang),
            vertical=True,
            className="flex-column",
            style={"padding": "0 1rem"},
        ),
        _lang_switcher(lang),
    ], style=SIDEBAR_STYLE)
