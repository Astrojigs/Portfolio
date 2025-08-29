# sections/projects/proximity_dublin.py
import json
import geopandas as gpd
import pandas as pd
import streamlit as st
from core.charts import GIS

SHP_PATH = "./core/references/gis/counties.shp"

@st.cache_data(show_spinner=False)
def load_geo(shp=SHP_PATH, simplify_m: int = 250):
    gdf = gpd.read_file(shp)                     # ❶ read once
    # pick a name column
    name_col = next((c for c in gdf.columns if "county" in c.lower()), None) or gdf.select_dtypes("object").columns[0]
    gdf = gdf[[name_col, "geometry"]].copy()

    gdf_m = gdf.to_crs(2157)                     # ❷ project to meters
    gdf_m["geometry"] = gdf_m.geometry.buffer(0) # fix invalids (safe no-op if fine)
    gdf_m["geometry"] = gdf_m.geometry.simplify(simplify_m, preserve_topology=True)  # ❸ simplify ~250 m

    gdf_wgs84 = gdf_m.to_crs(4326)               # ❹ back to WGS84 for the web map
    geojson = json.loads(gdf_wgs84.to_json())    # ❺ small payload (only name + geometry)

    return gdf_wgs84, gdf_m, name_col, geojson

def render():
    gdf_wgs84, gdf_m, name_col, geojson = load_geo()

    # Proximity (fast): centroid + edge distances in km
    dublin = gdf_m.loc[gdf_wgs84[name_col].str.contains("Dublin", case=False, na=False), "geometry"].unary_union
    df = pd.DataFrame({
        "County": gdf_wgs84[name_col].astype(str),
        "Distance_to_Dublin_centre_km": gdf_m.geometry.centroid.distance(dublin.centroid) / 1000,
        "Distance_to_Dublin_edge_km": gdf_m.geometry.distance(dublin) / 1000,
    }).round(1)

    # Use simplified in-memory GeoJSON (fast) + lock interactivity + disable animation
    gis = GIS(layers=[{
        "map_name": "ireland_counties",
        "source": geojson,
        "source_type": "geojson",
        "name_field": name_col,
    }])

    gis.plot(
        df,
        county_col="County",
        value_col="Distance_to_Dublin_centre_km",
        cmap="summer_r",
        cmap_steps=7,
        visual_map=True,
        map_title="GIS Ireland — Distance to Dublin (km)",
        label_on_hover=True,
        label_size=10,
        height="600px",
        # Perf helpers:
        extra_series_opts={
            "roam": False,          # avoid accidental pans
            "animation": False,     # faster first paint
            "progressive": 0        # turn off progressive calc overhead
        },

    )
