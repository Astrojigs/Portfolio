# core/components.py
from typing import List
import streamlit as st
from core.utils import custom_container, chips, custom_write


def project_card(title: str, caption: str, tags: List[str], url: str, url_name: str, summary: str, image_url: str,
                 image_caption: str):
    with custom_container(key=title, bg="#ffffff",
                          accent="#FF8C00", elevation=2, hover_elevation=4):
        left, right = st.columns([1.5, 1], vertical_alignment='center')

        with left:
            # Title
            st.subheader(title)
            # sub title(caption)
            st.caption(caption)

            tags_col, link_col = st.columns([3, 1], vertical_alignment='center')
            # tags
            with tags_col:
                chips(tags, variant="alt", size="md")

            # link
            with link_col:

                # if url starts with https://, then use this, else point to st.Page from session_state
                if url.startswith("https"):
                    st.markdown(f"[{url_name}]({url})")
                elif url.startswith("projects-"): # if it points to a project (inside the portfolio..)
                    if "pages" in st.session_state and url in st.session_state['pages']:
                        st.page_link(st.session_state['pages'][url], label="📖 :red[View details]")
                    else:
                        st.caption("Details page coming soon")
                else:
                    st.warning("`url` given does not point to a project.")

            # Summary
            custom_write("Summary", type='h5', color='gray')
            st.write(summary)

        with right:
            st.image(image_url, caption=image_caption, use_container_width=True)
