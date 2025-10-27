from dash import Input, Output, callback, html
from components.graphs import create_prague_map
from data_config import DATA_PATHS
from utils.data_loader import read_file
from dash import dcc
import dash

def get_prague_districts_lookup():
    df = read_file(str(DATA_PATHS.prague_districts))
    df = df.to_crs(4326)
    df["id"] = df.index
    df["name"] = df["nazev_1"].fillna("Unknown")
    return df[["id", "name"]]


@callback(
    Output("url", "href"),
    Input("prague-map", "clickData"),
)
def redirect_to_selected_district(click_data):
    if click_data and click_data.get("points"):
        location_id = click_data["points"][0]["location"]
        lookup_df = get_prague_districts_lookup()
        district_row = lookup_df[lookup_df["id"] == location_id]
        if not district_row.empty:
            district_name = district_row["name"].iloc[0]
            return "/district-detail" + f"?district={district_name}"
        else:
            raise dash.exceptions.PreventUpdate
    raise dash.exceptions.PreventUpdate
