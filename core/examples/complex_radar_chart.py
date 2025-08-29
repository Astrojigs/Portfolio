# core/examples/complex_radar_chart.py
import streamlit as st
from core.charts import ECharts


def render():
    indicators = [
        {"name": "Rent Affordability", "max": 100},
        {"name": "Salary Index", "max": 100},
        {"name": "Commute Ease", "max": 100},
        {"name": "Safety", "max": 100},
        {"name": "Green Space", "max": 100},
        {"name": "Nightlife", "max": 100},
        {"name": "Tech Hiring", "max": 100},
        {"name": "Healthcare Access", "max": 100},
    ]
    series_names = ["Dublin", "Cork", "Galway", "Limerick"]
    data = [
        [40, 80, 65, 58, 60, 90, 95, 85],
        [55, 68, 72, 70, 66, 70, 70, 78],
        [58, 62, 75, 68, 76, 72, 60, 75],
        [60, 58, 78, 62, 72, 65, 55, 73],
    ]
    palette = ["#2563eb", "#22c55e", "#eab308", "#ef4444"]

    ECharts.radar(
        indicators=indicators,
        data=data,
        series_names=series_names,
        height="460px",

        # Title small & tight to the top so legend fits beneath
        title=None,

        # 👇 Legend centered above the chart
        legend={
            "data": series_names,
            "left": "center",
            "top": 28,  # adjust if title is bigger
            "orient": "horizontal",
            "padding": 0,
            "itemGap": 10,
            "itemWidth": 10,
            "itemHeight": 10,
            "textStyle": {"fontSize": 11}
        },

        # 👇 Make axis labels smaller & nudge them closer to the edge
        radar={
            "indicator": indicators,
            "center": ["50%", "57%"],  # push chart down to make room for legend
            "radius": "66%",  # slightly smaller so labels don't clip
            "splitNumber": 5,
            "axisName": {"fontSize": 10},  # ECharts 5+
            "nameGap": 10,  # distance from axis end
            # Fallback for older ECharts (some wrappers use this key):
            "name": {"textStyle": {"fontSize": 10}}
        },

        color=palette,
        tooltip={"confine": True, "trigger": "item"},
        # toolbox={"feature": {"saveAsImage": {"title": "Save"}, "restore": {}}, "right": 6, "top": "middle"},
    )
    st.caption("Legend centered above; indicator labels reduced to 10pt. Tweak legend.top / radar.center if needed.")
