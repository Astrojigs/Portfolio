import streamlit as st
from core.utils import custom_container, custom_write, hero_video
from core.examples import dublin_proximity_gis, complex_radar_chart


def render():
    # custom_write('Gallery', type='h2', color='gray')

    c1, c2 = st.columns([3, 4], vertical_alignment='top', border=False)
    with c1:
        # Title
        st.write("# Gallery")
        st.caption("Here are some examples of what I do")
    with c2:
        with custom_container(key="Manim example", bg="#ffffff", hover_lift_px=3, radius="20px", padding="40px"):
            custom_write("Physics - Superposition in Motion", color='gray', type='h4')
            custom_write("Made using <i><b>Manim<b/><i/>", color='gray', type='caption')

            hero_video(path="./core/references/gifs/Manim Example.mp4",
                       mp4_path="./core/references/gifs/Manim Example.mp4")

        st.caption(':red[**Note**]: *Some **Gallery** examples use :blue[dummy data] and do not represent '
                   'real world statistics.*')

    with c1:
        # GIS example
        with custom_container(key='GIS example', hover_lift_px=3, radius="30px", padding="10px"):
            dublin_proximity_gis.render()

    with c2:
        # Echarts example
        with custom_container(key='complex radar chart', hover_lift_px=3, radius="100px", padding="40px"):
            complex_radar_chart.render()

    with c1:
        with custom_container(key='rl example', hover_lift_px=3, radius="20px", padding="10px"):
            rl_repo_link = "https://github.com/Astrojigs/LunarLander-Agent"
            custom_write("Reinforcement Learning - Lunar Lander", color='gray', type='h4')
            st.page_link(rl_repo_link, label="🪄 :red[Link to Repository]", icon=":material/cognition:")
            st.image("./core/references/gifs/reinforcement learning example.gif")

    # with c2:
    with custom_container(key="Barnes-Hut Example"):

        st.write("### Barnes–Hut N-Body (2D)")
        st.page_link(page=st.session_state['pages']['projects-barnes_hut'], label=":red[See more...] :material/link:",)
        # st.page_link(page="https://github.com/Astrojigs/Orbital-simulations/"
        #                   "blob/main/Barnes-hut%20Algorithm%20Animations.ipynb", label=":blue[Github Notebook] :material/link:")
        sub_c1, sub_c2 = st.columns([1, 1])
        with sub_c1:
            custom_write("<b>Example 1</b> (<i>without Quadtree</i>)")
            hero_video("./core/references/Project Files/Barnes-Hut/compressed/ep9600_compressed.mp4",
                       mp4_path="./core/references/Project Files/Barnes-Hut/compressed/ep9600_compressed.mp4")
        with sub_c2:

            custom_write("<b>Example 2</b> (<i>with Quadtree</i>)")
            hero_video('./core/references/Project Files/Barnes-Hut/compressed/ep2_quadtree_compressed.mp4',
                       mp4_path="./core/references/Project Files/Barnes-Hut/compressed/ep2_quadtree_compressed.mp4")

    # more example coming in
    custom_write('More examples coming in...', type='h4', color='gray')
