import streamlit as st
from core import utils
import pandas as pd
from core.charts import ECharts
import base64





def show_radar_skills():
    # --- Define Skills & Levels ---
    skills = [
        {"name": "Python", "max": 100},
        {"name": "Data Analysis", "max": 100},
        {"name": "Visualization (ECharts/Matplotlib)", "max": 100},
        {"name": "SQL", "max": 100},
        {"name": "Machine Learning", "max": 100},
        {"name": "Cloud (AWS)", "max": 100},
        {"name": "Data Structures & Algorithms", "max": 100},
    ]

    # Your own scores (0–100 scale)
    my_scores = [95, 90, 92, 85, 80, 75, 88]

    # Optional: a "target" profile for comparison
    target_scores = [100, 95, 95, 90, 90, 85, 90]

    # --- Display Radar Chart ---
    ECharts.radar(
        indicators=skills,
        data=[my_scores, target_scores],  # multiple series if you want comparison
        series_names=["Jigar", "Target Profile"],
        height="400px",
        series=[{
            "type": "radar",
            "data": [
                {
                    "value": my_scores,
                    "name": "Jigar",
                    "itemStyle": {"color": "red"},
                    "areaStyle": {"color": "rgba(255,0,0,0.1)"},  # red, 30% opacity
                    "lineStyle": {"color": "red", "width": 2}
                },
                {
                    "value": target_scores,
                    "name": "Target Profile",
                    "itemStyle": {"color": "orange"},
                    "areaStyle": {"color": "rgba(255,165,0,0.1)"},  # orange, 30% opacity
                    "lineStyle": {"color": "orange", "width": 2}
                }
            ]
        }]
    )


def show_pie():
    df = pd.DataFrame({
        "Skill": ["Python", "SQL", "Visualization", "Machine Learning", "Cloud (AWS)", "Finance"],
        "Level": [95, 85, 92, 80, 75, 88]
    })
    autumn_colors = [
        "#D2691E",  # Chocolate brown
        "#FF8C00",  # Dark orange
        "#FFA500",  # Orange
        "#FFD700",  # Golden yellow
        "#B22222",  # Firebrick red
        "#8B4513"  # Saddle brown
    ]
    ECharts.pie(
        df,
        names="Skill",
        values="Level",
        # title="Skills Breakdown",   # ❌ remove this line to hide title
        radius="70%",  # outer radius
        inner_radius="40%",  # makes it a donut
        border_radius=8,  # round edges
        label_outside=True,  # labels with leader lines
        legend_orient="vertical",
        legend_left="right",
        height="200px",
        color=autumn_colors,
        legend={"show": False},  # ❌ hide legend
        label_font_size=10
    )


def render():
    # Title
    utils.custom_write("Jigar Patel's Portfolio", type='h1')
    # Caption
    utils.custom_write('Everything there is to know about me.', type='para')
    st.divider()

    # Description ------------------
    image_column, description_column = st.columns([1, 2])
    # My image
    with image_column:
        # Usage
        st.image("./core/references/images/ProfilePic no background.png", width=300)
        st.divider()
    with description_column:
        utils.custom_write("Who Am I?", type='h2', color='gray')

        utils.custom_write("""
        <span style="font-size:16px; line-height:1.8;">
        👋 Hi, I’m <b style="color:#FF8C00;">Jigar Patel</b> — a <b>Data Analyst</b> and <b>Python Developer</b> based in Ireland, 
        with a background in <b>Physics (B.Sc.)</b> and <b>Data Science & Analytics (M.Sc.)</b>.  
        <br>
        📊 I specialize in building <b>data-driven solutions</b> that bring clarity to complex problems.  
        My work spans from developing <b>interactive dashboards</b> (Streamlit, Python, SQL, AWS)  
        to applying <b>quantitative finance models</b> and advanced <b>statistical techniques</b> 
        for real-world insights.  
        <br>
        🌌 Beyond work, I enjoy <b>astronomy</b>, <b>finance</b>, and <b>AI experimentation</b>,  
        where I combine <b>technical rigor</b> with <b>creativity</b> to explore new ideas.  
        <br>
        </span>
        """, type='caption')

        # --- Technical Skills
        utils.custom_write('Technical Skills', type='h4', color='gray')

        radar_col, pie_col = st.columns(2)
        with radar_col:
            show_radar_skills()
        with pie_col:
            show_pie()

        with utils.custom_container(shadow=True):
            st.subheader("Finance Portfolio Optimizer")
            st.write("Analyzes S&P500 assets to build efficient frontiers using Python + Pandas.")
            st.button("View Project")
