# sections/projects/proximity_dublin.py
import streamlit as st
import geopandas as gpd
import pandas as pd
from core.charts import GIS
from core.utils import custom_write
SHP_PATH = "./core/references/gis/counties.shp"


@st.cache_data(show_spinner=False)
def load_gdf(shp_path=SHP_PATH):
    gdf = gpd.read_file(shp_path)
    # Detect a county name field (works for most Irish counties layers)
    text_cols = [c for c in gdf.columns if gdf[c].dtype == object]
    preferred = [c for c in text_cols if
                 ("county" in c.lower()) or (c.lower() in {"name", "countyname", "eng_name", "english", "en_name"})]
    name_field = None
    for c in preferred + text_cols:
        if gdf[c].nunique() >= 20:  # expect 26+ distinct county-like names
            name_field = c
            break
    if not name_field:
        name_field = text_cols[0]  # fallback

    # Reproject to Irish Transverse Mercator for accurate metre distances
    gdf_2157 = gdf.to_crs(2157)
    return gdf, gdf_2157, name_field


def _build_proximity_df(gdf_wgs84: gpd.GeoDataFrame, gdf_2157: gpd.GeoDataFrame, name_field: str):
    # Find Dublin polygon (handles variations like 'Dublin City', 'Dublin')
    mask_dub = gdf_wgs84[name_field].astype(str).str.lower().str.contains("dublin")
    if not mask_dub.any():
        raise RuntimeError(f"Could not find a Dublin feature using field '{name_field}'.")
    # Union in case there are multiple Dublin features (city/county)
    dublin_geom = gdf_2157.loc[mask_dub, "geometry"].unary_union
    dublin_centroid = dublin_geom.centroid

    # Distances (in km)
    centroids = gdf_2157.geometry.centroid
    dist_centroid_km = centroids.distance(dublin_centroid) / 1000.0
    # Edge-to-edge distance: 0 if touching/overlapping Dublin
    dist_edge_km = gdf_2157.geometry.distance(dublin_geom) / 1000.0

    df = pd.DataFrame({
        "County": gdf_wgs84[name_field].astype(str).str.replace(r"\s+Co\.\s*", "", regex=True),
        "Distance_to_Dublin_centre_km": dist_centroid_km.round(1),
        "Distance_to_Dublin_edge_km": dist_edge_km.round(1),
    }).sort_values("Distance_to_Dublin_centre_km", ascending=True)

    # Proximity buckets (dummy categories)
    bins = [0, 50, 100, 150, 200, 1e9]
    labels = ["≤50 km", "50–100 km", "100–150 km", "150–200 km", "200+ km"]
    df["Proximity_bucket"] = pd.cut(df["Distance_to_Dublin_centre_km"], bins=bins, labels=labels, include_lowest=True)

    return df


def render():
    # custom_write("Proximity to Dublin — Irish Counties", type='h5', color='gray')
    gdf, gdf_2157, name_field = load_gdf()
    df = _build_proximity_df(gdf, gdf_2157, name_field)

    # Sidebar: choose distance metric
    metric = "Centroid distance (km)",
    value_col = "Distance_to_Dublin_centre_km"

    # # Show dummy dataframe for sanity check
    # st.dataframe(df, use_container_width=True)

    # Init GIS with your local shapefile (explicit name_field for reliable matching)
    gis = GIS(layers=[{
        "map_name": "ireland_counties",
        "source": SHP_PATH,
        "source_type": "file",
        "name_field": name_field,  # makes sure 'County' matches the layer’s attribute
    }])

    # Choropleth (continuous)
    gis.plot(
        df,
        county_col="County",
        value_col=value_col,
        cmap="inferno_r",  # or "Blues", ["#e8f2ff","#3b82f6",...]
        cmap_steps=7,
        visual_map=True,
        tooltip_title="Distance to Dublin (km)",
        map_title=f"Dublin Proximity Map",
        label_on_hover=True,
        label_size=11,
        height="440px",
        extra_geo_opts={  # affects the underlying geo component
            "roam": False,  # or "move" / "scale"
            "zoom": 1,  # keep initial zoom
            "scaleLimit": {"min": 1, "max": 1},
        },
        extra_series_opts={  # overrides the series' roam too
            "roam": False
        },
    )

    st.caption(
        "Notes: Distances use EPSG:2157 (Irish Transverse Mercator). "
        "Centroid distance measures centre-to-centre; edge-to-edge is 0 km for adjacent counties."
    )
