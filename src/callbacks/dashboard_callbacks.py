from dash import callback, Output, Input, State, ALL
import plotly.graph_objects as go

from src.components.graphs import create_single_district_map
from src.components.pages.dashboard import select_warning, district_select_warning
from src.configs.data_config import DATA_PATHS
from src.utils.districts.district_utils import get_points_in_district, get_district_polygons

from dash import dcc

from src.utils.polygons.polygon_utils import load_and_prepare_polygon_data
from src.utils.polygons.polygons_configs import POLYGON_LAYERS_CONFIGS
from src.utils.scatter.scatter_configs import SCATTER_LAYER_CONFIGS

ALL_DISTRICTS = sorted(list(get_district_polygons().keys()))

def get_czech_plural(count):
    if count == 1:
        return "objekt"
    elif 2 <= count <= 4:
        return "objekty"
    else:
        return "objektů"

@callback(
    Output('bar_chart_container', 'children'),
    Input('districts-dropdown', 'value'),
    Input("data-dropdown", "value"))
def update_output(districts, dataset):
    if not districts or len(districts) < 1 or not dataset:
        return select_warning()

    datasets_dic = DATA_PATHS.get_dataset_value_options()
    selected_dataset = next((item for item in datasets_dic if item['value'] == dataset), None)
    if selected_dataset:
        dataset_label = selected_dataset['label']
    else:
        dataset_label = "No dataset selected"

    data_points = []
    plural_forms = []
    for district in districts:
        count = len(get_points_in_district(district, dataset))
        data_points.append(count)
        plural_forms.append(get_czech_plural(count))

    colors = ['#3b82f6', '#6366f1', '#8b5cf6', '#a855f7', '#d946ef', '#ec4899', '#f43f5e']
    bar_colors = [colors[i % len(colors)] for i in range(len(districts))]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=districts,
        y=data_points,
        name=dataset_label,
        customdata=plural_forms,
        marker=dict(
            color=bar_colors,
            line=dict(color='rgba(255, 255, 255, 0.8)', width=2)
        ),
        text=data_points,
        textposition='outside',
        textfont=dict(size=12, color='#1e293b', family='Arial, sans-serif', weight='bold'),
        hovertemplate='<b style="font-size:16px; color:#1e293b;">📍 %{x}</b><br>' +
                      '<span style="color:#64748b;">━━━━━━━━━━━━━━━</span><br>' +
                      f'<b style="color:#3b82f6; font-size:14px;">{dataset_label}</b><br>' +
                      '<span style="font-size:20px; color:#059669; font-weight:bold;margin-top:5px"">%{y}</span> ' +
                      '<span style="color:#64748b; font-size:12px; margin-top:5px">%{customdata}</span><br>' +
                      '<extra></extra>'
    ))

    fig.update_layout(
        title=dict(
            text=f"Porovnání dat: {dataset_label}",
            font=dict(size=24, color='#1e293b', family='Arial, sans-serif', weight='bold'),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#f8fafc',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', color='#475569'),
        hovermode='closest',
        showlegend=False,
        margin=dict(l=60, r=40, t=80, b=80),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Arial, sans-serif",
            bordercolor="#cbd5e1",
            align="left"
        )
    )

    fig.update_xaxes(
        title_text="Městské části",
        title_font=dict(size=16, color='#334155', weight='bold'),
        tickfont=dict(size=12, color='#475569'),
        showgrid=False,
        showline=True,
        linewidth=2,
        linecolor='#cbd5e1'
    )

    fig.update_yaxes(
        title_text=f"Počet: {dataset_label}",
        title_font=dict(size=16, color='#334155', weight='bold'),
        tickfont=dict(size=12, color='#475569'),
        showgrid=True,
        gridwidth=1,
        gridcolor='#e2e8f0',
        showline=True,
        linewidth=2,
        linecolor='#cbd5e1'
    )

    return dcc.Graph(
        id={'type': 'district-bar-chart', 'index': 0},
        figure=fig,
        config={
            'displayModeBar': False,
            'displaylogo': False
        },
        style={'height': '600px'}
    )

@callback(
    Output('district_map_container', 'children'),
    Input({'type': 'district-bar-chart', 'index': ALL}, 'clickData'),
    State('data-dropdown', 'value'),
    prevent_initial_call=True
)
def create_district_map(click_data, dataset):
    if click_data and click_data[0]:
        clicked_district = click_data[0]['points'][0]['x']
        print(f"Clicked district: {clicked_district}, Dataset: {dataset}")
        if dataset in SCATTER_LAYER_CONFIGS:
            config = SCATTER_LAYER_CONFIGS[dataset]
            filtered_data = get_points_in_district(clicked_district, dataset)
            scatters = {dataset: {
                "data": filtered_data,
                "lon_column": "geometry",
                "lat_column": "geometry",
                "marker_size": config["marker_size"],
                "marker_color": config["marker_color"],
                "marker_opacity": config["marker_opacity"],
                'legend_group': config['legend_group'],
                "name": config["name"],
            }}
            fig = create_single_district_map(district=clicked_district, scatters=scatters, polygons={}, showlegend=False)
            return dcc.Graph(
                id="single-district-map",
                figure=fig,
                config={
                    'displayModeBar': False,
                },
                style={"marginBottom": "60px", "width": "100%"}
            )
            return fig
        if dataset in POLYGON_LAYERS_CONFIGS:
            config = POLYGON_LAYERS_CONFIGS[dataset]
            df, geojson = load_and_prepare_polygon_data(clicked_district, dataset)
            polygons = {dataset: {
                "geojson": geojson,
                "df": df,
                "background_color": config["background_color"],
                'legend_group': config['legend_group'],
                'name': config['name'],
            }}
            fig = create_single_district_map(district=clicked_district, scatters={}, polygons=polygons, showlegend=False)
            return dcc.Graph(
                id="single-district-map",
                figure=fig,
                config={
                    'displayModeBar': False,
                },
                style={"marginBottom": "60px", "width": "100%"}
            )
    return district_select_warning()

@callback(
    Output('districts-dropdown', 'value'),
    Input('select-all-districts-btn', 'n_clicks'),
    prevent_initial_call=True
)
def select_all_districts(n_clicks):
    return ALL_DISTRICTS
