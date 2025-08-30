import streamlit as st
from core.utils import custom_container, custom_write, chips, hero_video


def render():
    custom_write('Barnes Hut Algorithms', color="orange", type='h2')

    with custom_container(key="Barnes-Hut Example"):
        c1, c2 = st.columns([1, 1])
        with c1:
            hero_video("./core/references/Project Files/Barnes-Hut/ep2_web.mp4",
                       mp4_path="./core/references/Project Files/Barnes-Hut/ep2_web.mp4")
        with c2:
            hero_video('./core/references/Project Files/Barnes-Hut/ep2_quadtree_web.mp4',
                       mp4_path="./core/references/Project Files/Barnes-Hut/ep2_quadtree_web.mp4")

    custom_write("<i>More details coming in soon</i>...", color='gray')
