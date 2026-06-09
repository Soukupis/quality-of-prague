from dash import callback, Output, Input, State, ALL
import plotly.graph_objects as go

from src.components.graphs import create_single_district_map
from src.components.pages.dashboard import select_warning, district_select_warning
from src.configs.data_config import DATA_PATHS
from src.utils.districts.district_utils import get_points_in_district, get_district_polygons, get_district_areas_km2
from src.i18n import t

from dash import dcc

from src.utils.polygons.polygon_utils import load_and_prepare_polygon_data
from src.utils.polygons.polygons_configs import POLYGON_LAYERS_CONFIGS
from src.utils.scatter.scatter_configs import SCATTER_LAYER_CONFIGS

ALL_DISTRICTS = sorted(list(get_district_polygons().keys()))


def _get_plural(count, lang):
    if lang == "en":
        return t("plural_object_1", lang) if count == 1 else t("plural_object_5p", lang)
    if count == 1:
        return t("plural_object_1", lang)
    elif 2 <= count <= 4:
        return t("plural_object_2_4", lang)
    else:
        return t("plural_object_5p", lang)


@callback(
    Output("bar_chart_container", "children"),
    Input("districts-dropdown", "value"),
    Input("data-dropdown", "value"),
    Input("normalization-mode", "value"),
    Input("lang-store", "data"),
)
def update_output(districts, dataset, normalization_mode, lang):
    lang = lang or "cs"
    if not districts or len(districts) < 1 or not dataset:
        return select_warning(lang)

    datasets_dic = DATA_PATHS.get_dataset_value_options()
    selected_dataset = next((item for item in datasets_dic if item["value"] == dataset), None)
    dataset_label = selected_dataset["label"] if selected_dataset else dataset

    use_density = normalization_mode == "density"
    areas_km2 = get_district_areas_km2() if use_density else {}

    raw_counts = [len(get_points_in_district(d, dataset)) for d in districts]

    if use_density:
        data_points = [
            round(count / areas_km2[d], 4) if areas_km2.get(d, 0) > 0 else 0.0
            for count, d in zip(raw_counts, districts)
        ]
        text_values = [f"{v:.2f}" for v in data_points]
        custom_data = [
            f"{_get_plural(raw_counts[i], lang)} / km² (total {raw_counts[i]} in {areas_km2.get(d, 0):.1f} km²)"
            if lang == "en" else
            f"objektů / km² (celkem {raw_counts[i]} v ploše {areas_km2.get(d, 0):.1f} km²)"
            for i, d in enumerate(districts)
        ]
        y_axis_label = t("chart_y_density", lang, label=dataset_label)
        chart_title = t("chart_title_density", lang, label=dataset_label)
    else:
        data_points = raw_counts
        text_values = [str(v) for v in data_points]
        custom_data = [_get_plural(c, lang) for c in raw_counts]
        y_axis_label = t("chart_y_count", lang, label=dataset_label)
        chart_title = t("chart_title_count", lang, label=dataset_label)

    colors = ["#3b82f6", "#6366f1", "#8b5cf6", "#a855f7", "#d946ef", "#ec4899", "#f43f5e"]
    bar_colors = [colors[i % len(colors)] for i in range(len(districts))]

    if use_density:
        hover_template = (
            '<b style="font-size:16px; color:#1e293b;">📍 %{x}</b><br>'
            '<span style="color:#64748b;">━━━━━━━━━━━━━━━</span><br>'
            f'<b style="color:#3b82f6; font-size:14px;">{dataset_label}</b><br>'
            '<span style="font-size:20px; color:#059669; font-weight:bold;">%{y:.4f}</span> '
            '<span style="color:#64748b; font-size:12px;">obj/km²</span><br>'
            '<span style="color:#94a3b8; font-size:11px;">%{customdata}</span><br>'
            "<extra></extra>"
        )
    else:
        hover_template = (
            '<b style="font-size:16px; color:#1e293b;">📍 %{x}</b><br>'
            '<span style="color:#64748b;">━━━━━━━━━━━━━━━</span><br>'
            f'<b style="color:#3b82f6; font-size:14px;">{dataset_label}</b><br>'
            '<span style="font-size:20px; color:#059669; font-weight:bold;margin-top:5px">%{y}</span> '
            '<span style="color:#64748b; font-size:12px; margin-top:5px">%{customdata}</span><br>'
            "<extra></extra>"
        )

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=districts, y=data_points, name=dataset_label,
        customdata=custom_data,
        marker=dict(color=bar_colors, line=dict(color="rgba(255,255,255,0.8)", width=2)),
        text=text_values, textposition="outside",
        textfont=dict(size=12, color="#1e293b", family="Arial, sans-serif", weight="bold"),
        hovertemplate=hover_template,
    ))

    fig.update_layout(
        title=dict(
            text=chart_title,
            font=dict(size=24, color="#1e293b", family="Arial, sans-serif", weight="bold"),
            x=0.5, xanchor="center",
        ),
        plot_bgcolor="#f8fafc", paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", color="#475569"),
        hovermode="closest", showlegend=False,
        margin=dict(l=60, r=40, t=80, b=80),
        hoverlabel=dict(bgcolor="white", font_size=13, font_family="Arial, sans-serif",
                        bordercolor="#cbd5e1", align="left"),
    )
    fig.update_xaxes(
        title_text=t("chart_x_axis", lang),
        title_font=dict(size=16, color="#334155", weight="bold"),
        tickfont=dict(size=12, color="#475569"),
        showgrid=False, showline=True, linewidth=2, linecolor="#cbd5e1",
    )
    fig.update_yaxes(
        title_text=y_axis_label,
        title_font=dict(size=16, color="#334155", weight="bold"),
        tickfont=dict(size=12, color="#475569"),
        showgrid=True, gridwidth=1, gridcolor="#e2e8f0",
        showline=True, linewidth=2, linecolor="#cbd5e1",
    )

    return dcc.Graph(
        id={"type": "district-bar-chart", "index": 0},
        figure=fig,
        config={"displayModeBar": False, "displaylogo": False},
        style={"height": "600px"},
    )


@callback(
    Output("district_map_container", "children"),
    Input({"type": "district-bar-chart", "index": ALL}, "clickData"),
    State("data-dropdown", "value"),
    State("lang-store", "data"),
    prevent_initial_call=True,
)
def create_district_map(click_data, dataset, lang):
    lang = lang or "cs"
    if click_data and click_data[0]:
        clicked_district = click_data[0]["points"][0]["x"]
        if dataset in SCATTER_LAYER_CONFIGS:
            config = SCATTER_LAYER_CONFIGS[dataset]
            filtered_data = get_points_in_district(clicked_district, dataset)
            scatters = {dataset: {
                "data": filtered_data,
                "lon_column": "geometry", "lat_column": "geometry",
                "marker_size": config["marker_size"],
                "marker_color": config["marker_color"],
                "marker_opacity": config["marker_opacity"],
                "legend_group": config["legend_group"],
                "name": config["name"],
            }}
            fig = create_single_district_map(
                district=clicked_district, scatters=scatters, polygons={}, showlegend=False
            )
            return dcc.Graph(
                id="single-district-map", figure=fig,
                config={"displayModeBar": False},
                style={"marginBottom": "60px", "width": "100%"},
            )
        if dataset in POLYGON_LAYERS_CONFIGS:
            config = POLYGON_LAYERS_CONFIGS[dataset]
            df, geojson = load_and_prepare_polygon_data(clicked_district, dataset)
            polygons = {dataset: {
                "geojson": geojson, "df": df,
                "background_color": config["background_color"],
                "legend_group": config["legend_group"],
                "name": config["name"],
            }}
            fig = create_single_district_map(
                district=clicked_district, scatters={}, polygons=polygons, showlegend=False
            )
            return dcc.Graph(
                id="single-district-map", figure=fig,
                config={"displayModeBar": False},
                style={"marginBottom": "60px", "width": "100%"},
            )
    return district_select_warning(lang)


@callback(
    Output("districts-dropdown", "value"),
    Input("select-all-districts-btn", "n_clicks"),
    prevent_initial_call=True,
)
def select_all_districts(n_clicks):
    return ALL_DISTRICTS
