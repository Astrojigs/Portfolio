import streamlit as st
from core.utils import custom_container, custom_write


def render():
    custom_write('Gallery', type='h2', color='gray')

    # caption
    custom_write("Here are some examples of what I do", color='gray', type='caption')

    c1, c2 = st.columns([1.5, 1])

    with c1:
        # GIS example
        pass

    with c2:
        # Echarts example
        pass

    with c1:
        # Manim example
        pass
