from src.utils.districts.district_utils import get_points_in_district
from src.utils.scatter.scatter_colors import SUBWAY_ENTRANCES_LINE_COLORS, subway_entrances_color_to_rgba_points, subway_entrances_color_to_rgba_circles
from src.utils.scatter.scatter_configs import SCATTER_LAYER_CONFIGS
from src.utils.loaders.subway_loader import aggregate_metro_stations, calculate_station_circle_params
import plotly.graph_objects as go
import numpy as np

def build_scatter_config(district: str, layer_keys: list) -> dict:
    if not layer_keys:
        return {}

    scatters = {}
    for layer_key in layer_keys:
            if layer_key == "subway_entrances":
                subway_entrances = get_points_in_district(district, layer_key)
                if not subway_entrances.empty:
                    scatters[layer_key] = {
                        "type": "subway_entrances",
                        "data": subway_entrances
                    }
            elif layer_key in SCATTER_LAYER_CONFIGS:
                config = SCATTER_LAYER_CONFIGS[layer_key]
                filtered_data = get_points_in_district(district, layer_key)

                scatters[layer_key] = {
                    "data": filtered_data,
                    "lon_column": "geometry",
                    "lat_column": "geometry",
                    "marker_size": config["marker_size"],
                    "marker_color": config["marker_color"],
                    "marker_opacity": config["marker_opacity"],
                    'legend_group': config['legend_group'],
                    "name": config["name"],
                }
    return scatters

def build_single_line_station_trace(subway_data, line):
    df_line = subway_data[subway_data["vst_linka"] == line]
    if df_line.empty:
        return None

    return go.Scattermap(
        lon=df_line["geometry"].x,
        lat=df_line["geometry"].y,
        mode="markers",
        name=f"Stanice metra {line}",
        marker=dict(
            size=10,
            color=SUBWAY_ENTRANCES_LINE_COLORS.get(line, "gray"),
            opacity=0.9
        ),
        legendgroup="Doprava",
        text=df_line["vst_nazev"] + f" (Line {line})",
        hoverinfo="text"
    )

def build_single_line_traces(subway_data):
    traces = []
    for line in SUBWAY_ENTRANCES_LINE_COLORS.keys():
        trace = build_single_line_station_trace(subway_data, line)
        if trace:
            traces.append(trace)
    return traces

def build_half_transfer_station_trace(theta_half1,station, is_first_transfer, line=None, point_radius=0.0001, ):
    color = SUBWAY_ENTRANCES_LINE_COLORS.get(line, "gray")
    fill_color = subway_entrances_color_to_rgba_points.get(color, "rgba(128, 128, 128, 0.9)")

    center_lon_pt = station["geometry"].x
    center_lat_pt = station["geometry"].y
    lat_scale_pt = np.cos(np.radians(center_lat_pt))

    half1_lons = center_lon_pt + (point_radius / lat_scale_pt) * np.cos(theta_half1)
    half1_lats = center_lat_pt + point_radius * np.sin(theta_half1)
    half1_lons = np.append(half1_lons, [center_lon_pt])
    half1_lats = np.append(half1_lats, [center_lat_pt])

    return go.Scattermap(
                lon=half1_lons.tolist(),
                lat=half1_lats.tolist(),
                mode="lines",
                name=f"Transfer Station" if is_first_transfer else None,
                line=dict(width=1, color=color),
                fill="toself",
                showlegend=False,
                fillcolor=fill_color,
                text=station["vst_nazev"] + f" ({station['uzel_nazev']}: {station['vst_linka']})",
                hoverinfo="text"
            )

def build_single_point_transfer_station_trace(idx, station, transfer_stations):
    traces = []
    lines = station["vst_linka"].split(",")
    is_first_transfer = bool(idx == transfer_stations.index[0])

    line1 = lines[0].strip()
    theta_half1 = np.linspace(0, np.pi, 25)
    first_half_trace = build_half_transfer_station_trace(theta_half1, station, is_first_transfer, line1)
    traces.append(first_half_trace)

    line2 = lines[1].strip() if len(lines) > 1 else lines[0].strip()
    theta_half2 = np.linspace(np.pi, 2 * np.pi, 25)
    first_half_trace = build_half_transfer_station_trace(theta_half2, station, is_first_transfer, line2)
    traces.append(first_half_trace)

    return traces

def build_transfer_station_traces(subway_data):
    traces = []
    transfer_stations = subway_data[subway_data["vst_linka"].str.contains(",", na=False)]
    if not transfer_stations.empty:
        for idx, station in transfer_stations.iterrows():
            transfer_station_trace = build_single_point_transfer_station_trace(idx, station, transfer_stations)
            traces.extend(transfer_station_trace)
    return traces

def create_half_circle_traces(theta, center_lon, center_lat, radius, lat_scale, circle_color, fill_color, name):
    arc_lons = center_lon + (radius / lat_scale) * np.cos(theta)
    arc_lats = center_lat + radius * np.sin(theta)

    fill_lons = np.concatenate([arc_lons, [center_lon, arc_lons[0]]])
    fill_lats = np.concatenate([arc_lats, [center_lat, arc_lats[0]]])

    traces = []

    traces.append(go.Scattermap(
        lon=fill_lons.tolist(),
        lat=fill_lats.tolist(),
        mode="lines",
        name=name,
        showlegend=False,
        line=dict(width=0, color=circle_color),
        fill="toself",
        fillcolor=fill_color,
        text=name,
        hoverinfo="text"
    ))

    traces.append(go.Scattermap(
        lon=arc_lons.tolist(),
        lat=arc_lats.tolist(),
        mode="lines",
        showlegend=False,
        line=dict(width=2, color=circle_color),
        text=name,
        hoverinfo="text"
    ))

    return traces

def build_aggregated_station_trace(line, theta, center_lon, center_lat, radius, lat_scale, row):
    circle_color1 = SUBWAY_ENTRANCES_LINE_COLORS.get(line, "gray")
    fill_color1 = subway_entrances_color_to_rgba_circles.get(circle_color1, "rgba(128, 128, 128, 0.2)")
    circle_traces = create_half_circle_traces(
        theta, center_lon, center_lat, radius, lat_scale,
        circle_color1, fill_color1, row['uzel_nazev']
    )
    return circle_traces

def build_aggregated_station_traces(subway_data):
    aggregated = aggregate_metro_stations(subway_data)
    traces = []
    for _, row in aggregated.iterrows():
        center_lon, center_lat, radius, lat_scale = calculate_station_circle_params(row["geometry"])

        vst_linka_str = str(row['vst_linka']).strip()
        lines = [line.strip() for line in vst_linka_str.split(",")] if "," in vst_linka_str else [vst_linka_str]

        if len(lines) > 1:
            theta_half1 = np.linspace(0, np.pi, 100)
            first_aggregated_station_trace = build_aggregated_station_trace( lines[0],theta_half1, center_lon, center_lat, radius, lat_scale, row)
            traces.extend(first_aggregated_station_trace)

            theta_half2 = np.linspace(np.pi, 2*np.pi, 50)
            second_aggregated_station_trace = build_aggregated_station_trace(lines[1], theta_half2, center_lon, center_lat, radius,lat_scale, row)
            traces.extend(second_aggregated_station_trace)
        else:
            # Single-line station - full circle
            circle_color = SUBWAY_ENTRANCES_LINE_COLORS.get(lines[0], "orange")
            fill_color = subway_entrances_color_to_rgba_circles.get(circle_color, "rgba(255, 165, 0, 0.2)")
            theta = np.linspace(0, 2*np.pi, 100)
            circle_traces = create_half_circle_traces(
                theta, center_lon, center_lat, radius, lat_scale,
                circle_color, fill_color, row['uzel_nazev']
            )
            traces.extend(circle_traces)
    return traces

def build_subway_entrance_traces(subway_data):
    traces = []

    single_line_traces = build_single_line_traces(subway_data)
    traces.extend(single_line_traces)

    transfer_line_traces = build_transfer_station_traces(subway_data)
    traces.extend(transfer_line_traces)

    aggregated_line_traces = build_aggregated_station_traces(subway_data)
    traces.extend(aggregated_line_traces)

    return traces

