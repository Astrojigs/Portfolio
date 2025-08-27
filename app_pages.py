# # app_pages.py
# from dataclasses import dataclass
# from typing import Callable, Dict, List, Tuple
# import streamlit as st
#
# # Import your render callables
# import sections.home
# import sections.about_me
# import sections.contact
# import sections.projects.barnes_hut as proj_bh
# import sections.projects.dsna as proj_dsna
#
# @dataclass(frozen=True)
# class PageDef:
#     key: str                # stable key, e.g. "barnes_hut"
#     title: str              # shown in page metadata
#     url_path: str           # must be UNIQUE and FLAT (no "/")
#     icon: str               # emoji or :material/...:
#     render: Callable[[], None]
#     group: str              # grouping for st.navigation
#
# PAGES: List[PageDef] = [
#     PageDef("home",       "Home",                         "home",                 ":material/home:",            sections.home.render,     "Profile"),
#     PageDef("about",      "About Me",                     "about",                ":material/person:",          sections.about_me.render, "Profile"),
#     PageDef("barnes_hut", "Barnes–Hut N-Body",            "projects-barnes-hut",  ":material/auto_graph:",      proj_bh.render,           "Projects"),
#     PageDef("dsna",       "Data Structures & Algorithms", "projects-dsna",        ":material/developer_board:", proj_dsna.render,         "Projects"),
#     PageDef("contact",    "Contact",                      "contact",              ":material/mail:",            sections.contact.render,  "Other"),
# ]
#
# DEFAULT_KEY = "home"
#
# def build_navigation() -> Tuple[Dict[str, List[st.Page]], Dict[str, st.Page], Dict[str, str]]:
#     """
#     Returns:
#       groups_for_nav: dict[str, list[st.Page]]
#       pages_by_key:   dict[str, st.Page]           # use these with page_link/switch_page
#       routes_by_key:  dict[str, str]               # raw url_path strings (optional)
#     """
#     groups: Dict[str, List[st.Page]] = {}
#     pages_by_key: Dict[str, st.Page] = {}
#     routes_by_key: Dict[str, str] = {}
#
#     for p in PAGES:
#         page = st.Page(
#             p.render,
#             title=p.title,
#             icon=p.icon,
#             url_path=p.url_path,
#             default=(p.key == DEFAULT_KEY),
#         )
#         groups.setdefault(p.group, []).append(page)
#         pages_by_key[p.key] = page
#         routes_by_key[p.key] = p.url_path
#
#     return groups, pages_by_key, routes_by_key
#
# # Optional helper: pass in the pages_by_key dict you got from build_navigation()
# def goto(key: str, pages_by_key: Dict[str, st.Page]) -> None:
#     st.switch_page(pages_by_key[key])
