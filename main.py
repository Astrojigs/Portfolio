import streamlit as st
import streamlit_antd_components as sac
from core import utils
import sections


def config(page_title='Astrojigs Portfolio'):
    """
    configure main page title
    """
    st.set_page_config(layout='wide', page_title=page_title,
                       page_icon='./core/references/images/ProfilePic.jpeg')


def main():
    st.logo("./core/references/images/astrojigs logo.png")

    pages = {
        "Profile": [
            st.Page(sections.home.render, title="Home", icon=":material/home:",
                    url_path="home", default=False),
            st.Page(sections.about_me.render, title="About Me", icon=":material/person:",
                    url_path="about")
        ],
        "Projects": [st.Page(sections.projects.barnes_hut.render, title='Barnes-Hut', icon=":material/developer_board:",
                             url_path='projects-barnes_hut'),
                     st.Page(sections.projects.dsna.render, title='Data Structures and Algorithms',
                             icon=':material/auto_graph:',
                             url_path='projects-dsna')],
        "Other": [
            st.Page(sections.contact.render, title="Contact", icon=":material/mail:",
                    url_path="contact"),

        ]
    }
    config()

    pg = st.navigation(pages, position="sidebar", expanded=True)
    pg.run()  # <- do not manually call your render() functions elsewhere
    # with st.sidebar:
    #     utils.custom_write("Profile Sections")
    #     section = sac.menu([
    #         sac.MenuItem(label='Home'),
    #         sac.MenuItem(label='About Me'),
    #         sac.MenuItem(label='Projects'),
    #         sac.MenuItem(type='divider'),
    #         sac.MenuItem(label='Contact')
    #     ], color='dark'
    #     )
    #
    # if section == 'About Me':
    #     sections.about_me.render()
    # elif section == 'Home':
    #     sections.home.render()


if __name__ == '__main__':
    main()
