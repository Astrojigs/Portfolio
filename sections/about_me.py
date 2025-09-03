import streamlit as st
from core import utils
import pandas as pd

from core.cards import project_card
from core.utils import custom_container, chips, custom_write
from core.charts import ECharts


# -----------------------------
# Charts
# -----------------------------

def tech_stack():
    custom_write("My Tech Stack", type="h3", color="gray")

    st.markdown("""
    <!-- Devicon font (for Matplotlib icon) -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/devicon.min.css"/>

    <style>
      .ti-wrap{
        --gap:.75rem; --icon-size:28px;
        display:grid; grid-template-columns:repeat(auto-fit, minmax(140px,1fr));
        gap:var(--gap); margin-top:.5rem;
      }
      .ti-pill{
        display:flex; align-items:center; gap:.6rem;
        padding:.6rem .8rem; border-radius:999px;
        border:1px solid rgba(0,0,0,.08);
        background:rgba(0,0,0,.03);
      }
      [data-theme="dark"] .ti-pill{
        border-color:rgba(255,255,255,.10);
        background:rgba(255,255,255,.05);
      }
      .ti-pill img{ width:var(--icon-size); height:var(--icon-size); display:block; }
      .ti-icon{ font-size:var(--icon-size); line-height:1; }
      .ti-label{ font-size:.95rem; opacity:.95; }
    </style>

    <div class="ti-wrap">
      <!-- Python -->
      <div class="ti-pill">
        <img alt="Python" src="https://cdn.simpleicons.org/python/3776AB"/>
        <span class="ti-label">Python</span>
      </div>

      <!-- Streamlit -->
      <div class="ti-pill">
        <img alt="Streamlit" src="https://cdn.simpleicons.org/streamlit/FF4B4B"/>
        <span class="ti-label">Streamlit</span>
      </div>

      <!-- NumPy -->
      <div class="ti-pill">
        <img alt="NumPy" src="https://cdn.simpleicons.org/numpy/013243"/>
        <span class="ti-label">NumPy</span>
      </div>

      <!-- Pandas -->
      <div class="ti-pill">
        <img alt="Pandas" src="https://cdn.simpleicons.org/pandas/150458"/>
        <span class="ti-label">Pandas</span>
      </div>

      <!-- ECharts -->
      <div class="ti-pill">
        <img alt="ECharts" src="https://cdn.simpleicons.org/apacheecharts/AA344D"/>
        <span class="ti-label">ECharts</span>
      </div>

      <!-- QGIS -->
      <div class="ti-pill">
        <img alt="QGIS"
             src="https://cdn.simpleicons.org/qgis/589632"
             onerror="this.onerror=null;this.src='https://commons.wikimedia.org/wiki/Special:FilePath/QGIS_logo%2C_2017.svg';"/>
        <span class="ti-label">QGIS</span>
      </div>

      <!-- GeoPandas -->
      <div class="ti-pill">
        <img alt="GeoPandas"
             src="https://geopandas.org/en/stable/_static/logo/geopandas_icon.png"
             onerror="this.onerror=null;this.src='https://raw.githubusercontent.com/geopandas/geopandas/main/doc/source/_static/logo/geopandas_icon.png';"/>
        <span class="ti-label">GeoPandas</span>
      </div>

      <!-- OpenCV -->
      <div class="ti-pill">
        <img alt="OpenCV" src="https://cdn.simpleicons.org/opencv/5C3EE8"/>
        <span class="ti-label">OpenCV</span>
      </div>

      <!-- TensorFlow -->
      <div class="ti-pill">
        <img alt="TensorFlow" src="https://cdn.simpleicons.org/tensorflow/FF6F00"/>
        <span class="ti-label">TensorFlow</span>
      </div>

      <!-- PyTorch -->
      <div class="ti-pill">
        <img alt="PyTorch" src="https://cdn.simpleicons.org/pytorch/EE4C2C"/>
        <span class="ti-label">PyTorch</span>
      </div>

      <!-- Git -->
      <div class="ti-pill">
        <img alt="Git" src="https://cdn.simpleicons.org/git/F05032"/>
        <span class="ti-label">Git</span>
      </div>

      <!-- Docker -->
      <div class="ti-pill">
        <img alt="Docker" src="https://cdn.simpleicons.org/docker/2496ED"/>
        <span class="ti-label">Docker</span>
      </div>

      <!-- PostgreSQL -->
      <div class="ti-pill">
        <img alt="PostgreSQL"
             src="https://cdn.simpleicons.org/postgresql/4169E1"
             onerror="this.onerror=null;this.src='https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg';"/>
        <span class="ti-label">PostgreSQL</span>
      </div>

      <!-- MySQL -->
      <div class="ti-pill">
        <img alt="MySQL"
             src="https://cdn.simpleicons.org/mysql/4479A1"
             onerror="this.onerror=null;this.src='https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mysql/mysql-original.svg';"/>
        <span class="ti-label">MySQL</span>
      </div>

      <!-- Matplotlib (Devicon font) -->
      <div class="ti-pill">
        <i class="devicon-matplotlib-plain colored ti-icon" aria-label="Matplotlib"></i>
        <span class="ti-label">Matplotlib</span>
      </div>

      <!-- AWS (image with auto-fallback) -->
      <div class="ti-pill">
        <img alt="AWS"
             src="https://upload.wikimedia.org/wikipedia/commons/9/93/Amazon_Web_Services_Logo.svg"
             onerror="this.onerror=null;this.src='https://icongr.am/devicon/amazonwebservices-original.svg?size=64&color=FF9900';"/>
        <span class="ti-label">AWS</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


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
    # Header block (image + intro)
    col_img, col_text = st.columns([1, 2])
    with col_img:
        st.image("./core/references/images/ProfilePic no background.png", width=400)

    with col_text:
        with custom_container(key='Intro'):
            # ✨ Intro (closed span, better spacing)
            utils.custom_write("""
            <span style="font-size:16px; line-height:1.8;">
            I'm <b style="color:#FF8C00;">Jigar Patel</b> — a <b>Data Analyst</b> and <b>Python Developer</b> based in Ireland.
            </span>
            """, type='para')

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
        # Tech stack icons
        tech_stack()
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

    # Lunar Lander Agent
    project_card(
        title="Reinforcement Learning (Lunar Lander) — Python + TensorFlow",
        caption="Machine Learning • Artificial Intelligence • Algorithms • Policy • Agentic AI",
        tags=['Python', "TensorFlow", "Deep Learning", "Reinforcement Learning", 'Agent', "AI"],
        url="https://github.com/Astrojigs/LunarLander-Agent/tree",
        summary="A reinforcement learning agent trained on OpenAI Gym’s LunarLander-v2 that achieves "
                "reliable landings after ~760 episodes. Includes saved .h5 models and training artifacts."
                "*Unable to continue further training due to computational constraints*",
        url_name="🌐 GitHub ↗",
        image_url="./core/references/gifs/reinforcement learning example.gif",
        image_caption="Lander able to land after ~760 epochs."
    )
