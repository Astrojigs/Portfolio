import streamlit as st
from core import utils


def render():
    # Title
    utils.custom_write("Jigar Patel's Developer Portfolio", type='h2')
    # Caption
    utils.custom_write('Everything there is to know about me.', type='caption')
    st.divider()

    # Description ------------------
    image_column, description_column = st.columns([1, 2])
    # My image
    with image_column:
        st.image("./core/references/images/ProfilePic.jpeg")
    with description_column:
        with st.expander("# Who Am I?",expanded=True):
            utils.custom_write("""
            Hi, I’m Jigar Patel — a Data Analyst and Python Developer based in Ireland, with a background in Physics (B.Sc.) 
            and Data Science & Analytics (M.Sc.).<br><br>
            I specialize in building data-driven solutions that bring clarity to complex problems. My work spans from 
            developing interactive dashboards (using Streamlit, Python, SQL, AWS) to applying quantitative finance models 
            and statistical techniques for real-world insights.
            <br><br>
            Currently, I work at Mater Misericordiae University Hospital, Dublin, where I design and maintain clinical 
            analytics dashboards, streamline data pipelines, and collaborate with healthcare teams to turn raw data into 
            actionable outcomes.
            <br><br>
            Beyond work, I’m deeply curious about astronomy, finance, and AI, and I often channel that curiosity into side 
            projects — whether it’s building Python libraries, exploring astrophotography with my Nikon, or experimenting with portfolio optimization strategies.
            <br><br>
            I believe in combining technical rigor with creativity, and I enjoy sharing my work openly through my GitHub and 
            collaborative projects.
            """, type='para')
        with st.expander('Experience'):
            st.write('Experience')