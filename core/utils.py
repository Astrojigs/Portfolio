from typing import Literal
import streamlit as st


def custom_write(
        text: str,
        type: Literal['h1', 'h2', 'h3', 'h4', 'h5', 'para', 'caption'] = 'para',
        align: Literal['left', 'center', 'right', 'justify'] = 'center',
        color: str = 'black'
):
    """
    Write centered (or otherwise aligned) text in Streamlit using HTML.

    :param text:     The text to display (can contain &, <, > safely).
    :param type:     One of 'h1'–'h5', 'para' (normal paragraph) or 'caption' (small text).
    :param align:    Text alignment: 'left', 'center', 'right' or 'justify'.
    :param color:    Any valid CSS color (name, hex, rgb, etc.).
    """
    # map our logical types to HTML tags
    tag_map = {
        'h1': 'h1',
        'h2': 'h2',
        'h3': 'h3',
        'h4': 'h4',
        'h5': 'h5',
        'para': 'p',
        'caption': 'small'
    }
    tag = tag_map[type]

    # build the HTML
    html = f"""
    <div style="text-align: {align}; color: {color};">
      <{tag}>{text}</{tag}>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)
