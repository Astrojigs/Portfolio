# ./core/utils.py

import base64
from typing import Literal
# utils/containers.py
from contextlib import contextmanager
from uuid import uuid4
import streamlit as st
import re


def _sanitize_key(key: str) -> str:
    # valid CSS id chars only
    key = re.sub(r'[^a-zA-Z0-9_\-:.]', '-', key)
    return key or "card"


def _shadow(level: int) -> str:
    return {
        0: "0 0 0 rgba(0,0,0,0)",
        1: "0 4px 12px rgba(0,0,0,.12)",
        2: "0 8px 24px rgba(0,0,0,.16)",
        3: "0 14px 36px rgba(0,0,0,.20)",
        4: "0 22px 48px rgba(0,0,0,.24)",
    }.get(int(level or 0), "0 8px 24px rgba(0,0,0,.16)")


@contextmanager
def custom_container(
        *,
        key: str,  # ← REQUIRED for stability (e.g., "proj1")
        bg: str = "#ffffff",
        text_color: str | None = None,
        padding: str = "20px",
        radius: str = "14px",
        elevation: int = 2,  # 0–4
        hover_elevation: int = 3,  # 0–4
        hover_lift_px: int = 3,
        margin: str = "16px 0 28px",
        border: str | None = None,
        accent: str | None = None,
        accent_width: str = "4px",
        force_visible_shadow: bool = True,
        debug_outline: bool = False,
):
    """
    Stable, styled card container that wraps normal Streamlit widgets.
    Use a unique `key` per card and reuse the same key on every run.
    """
    sid = _sanitize_key(key)  # stable id per card
    marker_id = f"card-{sid}"

    block = st.container()
    with block:
        # 1) Insert the marker FIRST so CSS below will match immediately on this run
        st.markdown(f"<span id='{marker_id}'></span>", unsafe_allow_html=True)

        # 2) Inject CSS that targets ONLY the nearest block containing this marker
        nearest = (
            f"[data-testid='stVerticalBlock']"
            f":has(#{marker_id})"
            f":not(:has([data-testid='stVerticalBlock'] #{marker_id}))"
        )

        st.markdown(f"""
        <style>
          #{marker_id} {{ display:none; }}

          {nearest} {{
            position: relative;
            isolation: isolate;               /* keeps shadows independent */
            z-index: 0;
            background: {bg};
            {f"color:{text_color};" if text_color else ""}
            border-radius: {radius};
            padding: {padding};
            margin: {margin};
            box-shadow: {_shadow(elevation)};
            {"filter: drop-shadow(0 10px 22px rgba(0,0,0,.18));" if force_visible_shadow and elevation > 0 else ""}
            {f"border:{border};" if border else ""}
            {f"border-left:{accent_width} solid {accent};" if accent else ""}
            transition: transform .18s ease, box-shadow .18s ease, filter .18s ease;
            overflow: visible;                 /* don't clip shadows */
            background-clip: padding-box;
            {"outline: 2px dashed #f90;" if debug_outline else ""}
          }}

          {nearest}:hover {{
            transform: translateY(-{hover_lift_px}px);
            box-shadow: {_shadow(hover_elevation)};
            {"filter: drop-shadow(0 14px 32px rgba(0,0,0,.22));" if force_visible_shadow and hover_elevation > 0 else ""}
          }}

          /* remove extra inner padding some Streamlit wrappers add */
          {nearest} > div {{ padding: 0 !important; }}
        </style>
        """, unsafe_allow_html=True)

        yield block


def _inject_chip_css_once():
    if st.session_state.get("_chip_css_injected"):
        return
    st.session_state["_chip_css_injected"] = True
    st.markdown("""
    <style>
      .chip-wrap{
        display:flex; flex-wrap:wrap; gap:6px; row-gap:8px; align-items:center;
        margin:.25rem 0 .35rem 0;
      }
      .chip{
        display:inline-flex; align-items:center; gap:.4rem;
        padding:.28rem .6rem;
        border-radius:999px;
        font-size:.85rem; line-height:1;
        background:#f2f2f2; color:#333;
        border:1px solid rgba(0,0,0,.08);
        white-space:nowrap;
      }
      .chip.sm { font-size:.75rem; padding:.2rem .5rem; }
      .chip.lg { font-size:.95rem; padding:.38rem .75rem; }

      /* variants */
      .chip.alt  { background:#fff4e5; color:#8a4b00; border-color:#ffd7a8; }
      .chip.ok   { background:#e7f7ef; color:#116b3a; border-color:#bfe8d2; }
      .chip.info { background:#eef6ff; color:#0b5cad; border-color:#cfe3ff; }
      .chip.warn { background:#fff7e6; color:#a15a00; border-color:#ffe0b3; }
      .chip.dark { background:#2f2f2f; color:#f2f2f2; border-color:#00000033; }
      .chip.line { background:transparent; color:#555; border-color:#ccc; }

      .chip .ico { font-style:normal; opacity:.9; }
    </style>
    """, unsafe_allow_html=True)


def chips(
        items,
        *,
        variant: str = "default",  # default variant for all
        size: str = "md",  # "sm" | "md" | "lg"
        container=None,  # pass your card/container object; default = st
        wrap: bool = True,
):
    """
    Render a row of 'chips' (pills). Items can be strings or dicts:
      - "Python"
      - {"label":"AWS", "variant":"alt", "icon":"☁️"}
    """
    _inject_chip_css_once()
    target = container or st

    def one(item):
        if isinstance(item, str):
            label, v, icon = item, variant, None
        else:
            label = item.get("label", "")
            v = item.get("variant", variant)
            icon = item.get("icon")
        cls = "chip"
        if size in ("sm", "lg"): cls += f" {size}"
        if v and v != "default": cls += f" {v}"
        ico = f"<span class='ico'>{icon}</span>" if icon else ""
        return f"<span class='{cls}'>{ico}{label}</span>"

    html = "".join(one(i) for i in items)
    if wrap:
        html = f"<div class='chip-wrap'>{html}</div>"

    target.markdown(html, unsafe_allow_html=True)


# @contextmanager
# def custom_container(
#         bg="#ffffff",
#         padding="20px",
#         radius="14px",
#         shadow=True,
#         hover=True,
#         border=None,
# ):
#     uid = f"box-{uuid4().hex[:8]}"
#
#     # Style ONLY the nearest stVerticalBlock that contains the marker,
#     # excluding ancestors that also contain it.
#     nearest = f"[data-testid='stVerticalBlock']:has(#{uid}):not(:has([data-testid='stVerticalBlock'] #{uid}))"
#
#     st.markdown(f"""
#     <style>
#       /* hide marker */
#       #{uid} {{ display: none; }}
#
#       /* nearest container only */
#       {nearest} {{
#           background: {bg};
#           border-radius: {radius};
#           padding: {padding};
#           margin: 16px 0 28px;
#           {"box-shadow: 0 6px 18px rgba(0,0,0,0.12);" if shadow else ""}
#           {"border: 1px solid " + border + ";" if border else ""}
#           transition: transform .18s ease, box-shadow .18s ease;
#           overflow: hidden;
#       }}
#
#       /* optional hover lift on that same nearest block */
#       {nearest}:hover {{
#           {"transform: translateY(-3px); box-shadow: 0 12px 28px rgba(0,0,0,.16);" if hover else ""}
#       }}
#
#       /* avoid double inner padding from Streamlit wrappers */
#       {nearest} > div {{ padding: 0 !important; }}
#     </style>
#     """, unsafe_allow_html=True)
#
#     block = st.container()
#     with block:
#         st.markdown(f"<span id='{uid}'></span>", unsafe_allow_html=True)
#         yield block


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
