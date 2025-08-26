import base64
from typing import Literal
import streamlit as st
from contextlib import contextmanager


@contextmanager
def custom_container(bg_color="#ffffff", text_color="#333", shadow=True, padding="20px"):
    """
    Custom Streamlit container with shadow and styling.
    Usage:
        with custom_container(shadow=True):
            st.write("Inside container")
    """
    shadow_css = "box-shadow: 0 4px 12px rgba(0,0,0,0.15);" if shadow else ""
    style = f"""
        background-color: {bg_color};
        color: {text_color};
        border-radius: 12px;
        padding: {padding};
        margin: 15px 0;
        {shadow_css}
    """

    # Create the container
    container = st.container()

    with container:
        st.markdown(f"<div style='{style}'>", unsafe_allow_html=True)
        yield  # let user place Streamlit widgets here
        st.markdown("</div>", unsafe_allow_html=True)


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


def overlay_image_with_text(png_file, text="Hello, I’m Jigar"):
    bin_str = get_base64(png_file)
    html_code = f"""
    <style>
    .overlay-container {{
        position: relative;
        width: 100%;
        text-align: center;
        margin-top: 20px;
    }}
    .overlay-container img {{
        width: 400px;   /* control image size */
        height: auto;
        opacity: 0.9;   /* keep image visible */
    }}
    .overlay-text {{
        position: absolute;
        top: 50%;   /* center vertically */
        left: 50%;  /* center horizontally */
        transform: translate(-50%, -50%);
        color: white;
        font-size: 28px;
        font-weight: bold;
        text-shadow: 2px 2px 4px #000000;  /* make text readable */
    }}
    </style>

    <div class="overlay-container">
        <img src="data:image/png;base64,{bin_str}">
        <div class="overlay-text">{text}</div>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-position: top left; /* adjust position */
        background-size: 200px auto;
        background-repeat: no-repeat;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
