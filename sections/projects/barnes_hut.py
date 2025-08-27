import streamlit as st
from core.utils import custom_container, custom_write, chips


def render():
    st.write('# Barnes Hut Algorithms')
    project_card_orbits()





def project_card_orbits():
    GITHUB_URL = "https://github.com/Astrojigs/Orbital-simulations"
    # Raw GIF from your repo (fallback to a local image if you prefer)
    GIF_URL = ("https://raw.githubusercontent.com/Astrojigs/Orbital-simulations/"
               "main/Outputs/GIF/Barnes_hut_dual_gif.gif")

    with custom_container(key="proj_orbits", bg="#ffffff",
                          accent="#FF8C00", elevation=2, hover_elevation=4):
        left, right = st.columns([1.5, 1], vertical_alignment="center")

        with left:
            st.subheader("Orbital Simulations (Barnes–Hut)")
            st.caption("N-body gravitation • Quadtree acceleration • Potential fields")

            st.write(
                "Compact notebooks + utilities for bodies obeying the inverse-square law. "
                "Uses a Barnes–Hut quadtree to scale beyond O(N²) and ships with "
                "`astrojigs.py` (Point / Rectangle / Quadtree) for building custom sims."
            )

            chips(["Python", "NumPy", "Matplotlib", "Jupyter", "Barnes–Hut", "Quadtree"], variant="alt", size="sm")

            c1, c2 = st.columns(2)
            with c1:
                # External link (replace with st.link_button if available in your Streamlit)
                st.markdown(f"[🌐 GitHub ↗]({GITHUB_URL})")
            with c2:
                # Deep-link to your internal project page if you have one registered
                if "pages" in st.session_state and "barnes_hut" in st.session_state["pages"]:
                    st.page_link(st.session_state["pages"]["barnes_hut"], label="📖 View details")
                else:
                    st.caption("Details page coming soon")

        with right:
            st.image(GIF_URL, caption="Dual view: quadtree + particle motion", use_container_width=True)
