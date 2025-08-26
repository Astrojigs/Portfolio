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

    with st.sidebar:
        utils.custom_write("Profile Sections")
        section = sac.menu([
            sac.MenuItem(label='Home'),
            sac.MenuItem(label='About Me'),
            sac.MenuItem(label='Projects'),
            sac.MenuItem(type='divider'),
            sac.MenuItem(label='Contact')
        ], color='dark'
        )

    if section == 'About Me':
        sections.about_me.render()
    elif section == 'Home':
        sections.home.render()


def main():
    config()


if __name__ == '__main__':
    main()
