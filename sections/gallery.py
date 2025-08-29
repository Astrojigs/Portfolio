import streamlit as st
from core.utils import custom_container, custom_write
from core.examples import dublin_proximity_gis, complex_radar_chart


def render():
    custom_write('Gallery', type='h2', color='gray')

    # caption
    custom_write("Here are some examples of what I do", color='gray', type='caption')

    c1, c2 = st.columns([1.5, 1])

    with c1:
        # GIS example
        with custom_container(key='GIS example'):
            dublin_proximity_gis.render()

    with c2:
        # Echarts example
        with custom_container(key='complex radar chart'):
            complex_radar_chart.render()

    with c1:
        # Manim example
        pass

    # more example coming in
    custom_write('More examples coming in...',type='h4', color='gray')