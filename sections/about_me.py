import streamlit as st
from core import utils
import pandas as pd

from core.cards import project_card
from core.utils import custom_container, chips, custom_write
from core.charts import ECharts


# -----------------------------
# Charts
# -----------------------------
def show_radar_skills():
    skills = [
        {"name": "Python", "max": 100},
        {"name": "Data Analysis", "max": 100},
        {"name": "Visualization", "max": 100},
        {"name": "SQL", "max": 100},
        {"name": "Machine Learning", "max": 100},
        {"name": "Cloud (AWS)", "max": 100},
        {"name": "DS&A", "max": 100},
    ]
    my_scores = [95, 90, 92, 75, 90, 70, 88]

    ECharts.radar(
        indicators=skills,
        data=[my_scores],  # you're overriding series below
        height="400px",
        tooltip={"confine": False},  # prevent clipping
        series=[{
            "tooltip": {"confine": True},
            "type": "radar",
            "data": [{
                "value": my_scores,
                "name": "My Confidence Score",
                "itemStyle": {"color": "black"},
                "areaStyle": {"color": "rgba(252, 98, 3,0.07)"},
                "lineStyle": {"color": "pink", "width": 2}
            }]
        }]

    )

# -----------------------------
# Page
# -----------------------------
def render():
    # Title
    # utils.custom_write("Jigar Patel's Portfolio", type='h1')
    # utils.custom_write('Everything there is to know about me.', type='para')
    # st.divider()

    # Header block (image + intro)
    col_img, col_text = st.columns([1, 2])
    with col_img:
        st.image("./core/references/images/ProfilePic no background.png", width=400)

    with col_text:
        with custom_container(key='Intro') as c:
            utils.custom_write("Who Am I?", type='h2', color='black')

            # ✨ Intro (closed span, better spacing)
            utils.custom_write("""
            <span style="font-size:16px; line-height:1.8;">
            My name is Optimus Prime, we are autonomous robo....nah just kidding. I'm <b style="color:#FF8C00;">Jigar Patel</b> — a <b>Data Analyst</b> and <b>Python Developer</b> based in Ireland.
            </span>
            """, type='caption')

            custom_write('Education', color='gray', type='h4')
            # If st.badge isn't available in your build, use chips instead:
            st.badge(label='**M.Sc. Data Science & Analytics** :material/code:', color='red')
            st.badge(label="**B.Sc.  Physics** :material/orbit:", color='orange')

            utils.custom_write("Things I do", type='h4', color='gray')
            utils.custom_write("""
            <span style="font-size:16px; line-height:1.8;">
            📊 I specialize in building <b>data-driven solutions</b> that bring clarity to complex problems.
            My work spans from developing <b>interactive dashboards</b> (Streamlit, Python, SQL, AWS)
            to applying <b>quantitative finance models</b> and advanced <b>statistical techniques</b>
            for real-world insights.<br>
            🌌 Beyond work, I enjoy <b>astronomy</b>, <b>finance</b>, and <b>AI experimentation</b>, where I blend
            <b>technical rigor</b> with <b>creativity</b>.
            </span>
            """, type='caption', align='left')

    # Technical Skills block (charts side-by-side)
    # with custom_container(key='Charts') as c:
    st.divider()
    utils.custom_write('Technical Skills', type='h2', color='gray', align='center')
    skill_description_col, radar_col = st.columns(2)
    with skill_description_col:
        # with custom_container(key="Skill Description"):
        st.markdown("""
        **I build end-to-end data apps**—from ingestion and cleaning to modelling and interactive dashboards.
        
        - **Python:** pandas, NumPy, clean APIs, testable utilities.
        - **Data analysis:** exploratory stats, tidy pipelines, reproducible notebooks.
        - **Visualization:** interactive ECharts in Streamlit; Matplotlib for publication-quality plots.
        - **SQL:** modelling with joins/window functions, query tuning, clear schemas.
        - **Machine learning:** scikit-learn workflows, feature engineering, cross-validation, metrics you can trust.
        - **Cloud (AWS):** simple, reliable **EC2** deployments and storage when needed.
        - **DS & Algorithms:** write time/space-efficient code; I care about readability and asymptotics.

        I optimise for **clarity, correctness, and speed to insight**—and I ship visuals that non-technical 
        stakeholders can use.
                """)

        # Optional: tech “chips” row (uses your helper)
        chips(
            ["Python", "Pandas", "ECharts", "Matplotlib", "SQL", "scikit-learn", "AWS"],
            size="lg",
            container=skill_description_col,
        )

    with radar_col:
        with custom_container(key="radar chart"):
            utils.custom_write("My Confidence level in each field", type='h5', color='gray')
            show_radar_skills()

    # Projects teaser
    st.divider()
    utils.custom_write("📂 Some Noteworthy Projects", type='h3')

    # barnes hut Project
    project_card(
        title="Orbital Simulations (Barnes–Hut)",
        caption="N-body gravitation • Quadtree acceleration • Potential fields",
        tags=['Python', "Data Structure", "NumPy", "Matplotlib", "Quadtree"],
        url="projects-barnes_hut",  # "https://github.com/Astrojigs/Orbital-simulations",
        url_name="🌐 GitHub ↗",
        summary="Compact notebooks + utilities for bodies obeying the inverse-square law. "
                "Uses a Barnes–Hut quadtree to scale beyond O(N²) and ships with "
                "`astrojigs.py` (Point / Rectangle / Quadtree) for building custom sims.",
        image_url="https://raw.githubusercontent.com/Astrojigs/Orbital-simulations/"
                  "main/Outputs/GIF/Barnes_hut_dual_gif.gif",
        image_caption="Dual view: quadtree + particle motion"
    )

    # Aerial Images → Maps (CycleGAN)
    project_card(
        title="Aerial Images → Maps (CycleGAN)",
        caption="Image-to-image translation • Satellite imagery • CycleGAN",
        tags=["Python", "PyTorch", "CycleGAN", "Image2Image", "Computer Vision", "Satellite"],
        url="https://github.com/Astrojigs/Aerial-images-to-maps",
        url_name="🌐 GitHub ↗",
        summary=(
            "Translates aerial photos into map-style renderings with a cyclic GAN. "
            "Includes generator/discriminator architectures, training at 128×128 & 256×256, "
            "and losses (generator, discriminator, cycle, identity). Comes with an evaluation "
            "notebook and example results."
        ),
        image_url="https://github.com/Astrojigs/Aerial-images-to-maps/blob/main/Images/example%20images/128GAN_bs1_epoch50_results.png?raw=true",
        image_caption="Example output: aerial → map (CycleGAN)"
    )

    # Chaos, Pattern & Physics (3-body gravity → fractal basins)
    project_card(
        title="Chaos, Pattern & Physics (3-body gravity)",
        caption="Chaotic trajectories • Fractal basins • N-body toy model",
        tags=["Python", "Jupyter", "Simulation", "Physics", "Chaos Theory"],
        url="https://github.com/Astrojigs/Chaos-Pattern-and-Physics",
        url_name="🌐 GitHub ↗",
        summary=(
            "A playful physics simulation: one particle moves under gravity from three fixed “stars.” "
            "You colour each initial position by the star it eventually collides with, revealing beautiful "
            "fractal basins (100×100 → 2000×2000 grids) and sample trajectories."
        ),
        image_url="https://raw.githubusercontent.com/Astrojigs/Chaos-Pattern-and-Physics/main/NicePattern.png",
        image_caption="Fractal-like basin of attraction from the 3-body setup"
    )

    # Delhi Air Pollution — QGIS + SQL/PostGIS
    project_card(
        title="Delhi Air Pollution — QGIS + SQL/PostGIS",
        caption="Geospatial analysis • Wind & stubble burning • Temporal slices",
        tags=["QGIS", "PostgreSQL", "PostGIS", "GIS", "EDA"],
        url="https://github.com/Astrojigs/Delhi-air-pollution-reasons",
        url_name="🌐 GitHub ↗",
        summary=(
            "Spatial investigation of Delhi’s pollution: NASA fire points, wind vectors, terrain, and air-quality "
            "stations combined in QGIS/PostGIS. Builds 500 km views around Delhi and uses temporal slices "
            "(Aug–Nov) to show how post-harvest stubble fires and prevailing winds align with smog spikes."
        ),
        image_url="https://github.com/Astrojigs/Delhi-air-pollution-reasons/raw/main/Photos/terrain%20with%20wind%20data%20in%20Novemeber.png",
        image_caption="Wind vectors over terrain with incident fires (Nov)"
    )


    # with custom_container(key='P1', bg="#FAF3E0", accent="#FF8C00", elevation=2, hover_elevation=4) as c:
    #     c.subheader("Clinical Trials Dashboard")
    #     c.caption("Built with **Streamlit + AWS**, providing real-time insights into clinical trial data.")
    #     chips(["Streamlit", {"label": "AWS", "variant": "info", "icon": "☁️"}, "ECharts"], size="sm", container=c)
    #     c.button("🔍 View Project")
    #
    # with custom_container(key='P2', bg="#ffffff", elevation=2, hover_elevation=3, border="1px solid #eee") as c:
    #     c.subheader("Finance Portfolio Optimizer")
    #     c.caption("Efficient frontier & tangency tools in Python.")
    #     chips(
    #         ["Python", {"label": "Pandas", "variant": "line"}, {"label": "Portfolio", "variant": "warn", "icon": "💹"}],
    #         size="lg", container=c)
    #     c.button("📊 View Project")
