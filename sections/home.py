import pandas as pd
import streamlit as st
from core import utils
from core.charts import ECharts
from sections import about_me

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
        title="My Skill Radar",
        height="500px",
        series=[{
            "tooltip": {"confine": True},
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

    # --- Pie chart example ---
    ECharts.pie(
        df,
        names="Skill",
        values="Level",
        title="Skills Breakdown",
        radius="70%",  # outer radius
        inner_radius="40%",  # makes it a donut
        border_radius=8,  # round edges
        label_outside=True,  # labels with leader lines
        legend_orient="vertical",
        legend_left="right",
        height="500px"
    )


def render():
    """
    Renders the Home Page of the Portfolio
    :return:
        None
    """
    utils.hero_video(path="./core/references/gifs/DevTitle.webm")

    utils.custom_write("Python Developer / Data Analyst", type='h1')
    utils.custom_write(
        text="""
        I work on building techniques for data processing and data visualization in addition to building 
        automation pipelines.
        """, type='h4', color='gray')
    about_me.render()