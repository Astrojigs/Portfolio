import streamlit as st
from core import utils
import pandas as pd
from core.utils import custom_container, chips
from core.charts import ECharts


# -----------------------------
# Charts
# -----------------------------
def show_radar_skills():
    skills = [
        {"name": "Python", "max": 100},
        {"name": "Data Analysis", "max": 100},
        {"name": "Visualization (ECharts/Matplotlib)", "max": 100},
        {"name": "SQL", "max": 100},
        {"name": "Machine Learning", "max": 100},
        {"name": "Cloud (AWS)", "max": 100},
        {"name": "Data Structures & Algorithms", "max": 100},
    ]
    my_scores = [95, 90, 92, 75, 90, 70, 88]

    ECharts.radar(
        indicators=skills,
        data=[my_scores],  # you're overriding series below
        height="400px",
        tooltip={"confine": False},  # prevent clipping
        series=[{
            "type": "radar",
            "data": [{
                "value": my_scores,
                "name": "Jigar",
                "itemStyle": {"color": "red"},
                "areaStyle": {"color": "rgba(255,0,0,0.12)"},
                "lineStyle": {"color": "red", "width": 2}
            }]
        }]
    )


def show_pie():
    df = pd.DataFrame({
        "Skill": ["Python", "SQL", "Visualization", "Machine Learning", "Cloud (AWS)", "Finance"],
        "Level": [95, 85, 92, 80, 75, 88]
    })
    autumn_colors = ["#D2691E", "#FF8C00", "#FFA500", "#FFD700", "#B22222", "#8B4513"]

    ECharts.pie(
        df,
        names="Skill",
        values="Level",
        radius="70%",
        inner_radius="40%",  # donut
        border_radius=8,
        label_outside=True,
        height="240px",
        color=autumn_colors,
        legend={"show": False},
        label_font_size=10
    )


# -----------------------------
# Page
# -----------------------------
def render():
    # Title
    utils.custom_write("Jigar Patel's Portfolio", type='h1')
    utils.custom_write('Everything there is to know about me.', type='para')
    st.divider()

    # Header block (image + intro)
    col_img, col_text = st.columns([1, 2])
    with col_img:
        st.image("./core/references/images/ProfilePic no background.png", width=300)
        st.divider()

    with col_text:
        with custom_container(key='Intro') as c:
            utils.custom_write("Who Am I?", type='h2', color='black')

            # ✨ Intro (closed span, better spacing)
            utils.custom_write("""
            <span style="font-size:16px; line-height:1.8;">
            👋 Hi, I’m <b style="color:#FF8C00;">Jigar Patel</b> — a <b>Data Analyst</b> and <b>Python Developer</b> based in Ireland.
            </span>
            """, type='caption')

            c.write('##### Education')
            # If st.badge isn't available in your build, use chips instead:
            chips(
                [
                    {"label": "M.Sc. Data Science & Analytics", "variant": "alt", "icon": "🎓"},
                    {"label": "B.Sc. Physics", "variant": "info", "icon": "🔬"},
                ],
                size="sm",
                container=c
            )

            utils.custom_write("What I do", type='h4', color='gray')
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
    with custom_container(key='Charts') as c:
        utils.custom_write('Technical Skills', type='h4', color='gray', align='center')
        radar_col, pie_col = c.columns(2)
        with radar_col:
            show_radar_skills()
        with pie_col:
            show_pie()

    # Projects teaser
    utils.custom_write("📂 Projects", type='h2')
    with custom_container(key='P1', bg="#FAF3E0", accent="#FF8C00", elevation=2, hover_elevation=4) as c:
        c.subheader("Clinical Trials Dashboard")
        c.caption("Built with **Streamlit + AWS**, providing real-time insights into clinical trial data.")
        chips(["Streamlit", {"label": "AWS", "variant": "info", "icon": "☁️"}, "ECharts"], size="sm", container=c)
        c.button("🔍 View Project")

    with custom_container(key='P2', bg="#ffffff", elevation=2, hover_elevation=3, border="1px solid #eee") as c:
        c.subheader("Finance Portfolio Optimizer")
        c.caption("Efficient frontier & tangency tools in Python.")
        chips(
            ["Python", {"label": "Pandas", "variant": "line"}, {"label": "Portfolio", "variant": "warn", "icon": "💹"}],
            size="sm", container=c)
        c.button("📊 View Project")
