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
        with custom_container(key='GIS example', hover_lift_px=3, radius="60px", padding="20px"):
            dublin_proximity_gis.render()

    with c2:
        # Echarts example
        with custom_container(key='complex radar chart',hover_lift_px=3, radius="100px", padding="40px"):
            complex_radar_chart.render()

    c1, c2 = st.columns([1.5,1])
    with c1:
        # Manim example (website background color #f4f3ed)
        with custom_container(key="Manim example", bg="#ffffff",hover_lift_px=3, radius="40px", padding="40px"):
            custom_write("Physics - Superposition in Motion", color='gray', type='h4')
            custom_write("Made using <i><b>Manim<b/><i/>", color='gray', type='caption')

            hero_video(path="./core/references/gifs/Manim Example.mp4",
                       mp4_path="./core/references/gifs/Manim Example.mp4")

    # more example coming in
    custom_write('More examples coming in...', type='h4', color='gray')
