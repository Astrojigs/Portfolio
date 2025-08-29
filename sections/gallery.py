import streamlit as st
from core.utils import custom_container, custom_write, hero_video
from core.examples import dublin_proximity_gis, complex_radar_chart


def render():
    custom_write('Gallery', type='h2', color='gray')

    # caption
    custom_write("Here are some examples of what I do", color='gray', type='caption')

    c1, c2 = st.columns([1, 1.2])

    with c1:
        # GIS example
        with custom_container(key='GIS example'):
            dublin_proximity_gis.render()

    with c2:
        # Echarts example
        with custom_container(key='complex radar chart'):
            complex_radar_chart.render()

    # Manim example
    # with custom_container(key="Manim example", bg="#f4f3ed"):
    custom_write("Physics - Superposition in Motion", color='gray', type='h2')
    hero_video(path="./core/references/gifs/Manim Example.mp4",
               mp4_path="./core/references/gifs/Manim Example.mp4")

    # more example coming in
    custom_write('More examples coming in...', type='h4', color='gray')
