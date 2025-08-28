import streamlit as st
import sections


def config(page_title='Astrojigs Portfolio'):
    """
    configure main page title
    """
    st.set_page_config(layout='wide', page_title=page_title,
                       page_icon='./core/references/images/ProfilePic.jpeg')


def main():
    config()

    st.logo("./core/references/images/astrojigs logo.png")

    # ------------------- Pages ---------------------------
    home_page = st.Page(sections.home.render, title='Home', icon=':material/home:', url_path="home", default=True)

    # ---------- Project Pages --------------------
    barnes_hut_page = st.Page(sections.projects.barnes_hut.render, title='Barnes-Hut',
                              icon=":material/developer_board:",
                              url_path="projects-barnes_hut")
    cycle_gan_page = st.Page(sections.projects.cycle_gan.render, title='CycleGAN', url_path="projects-cyclegan",
                             icon=":material/landscape_2:")

    # Other pages
    contact_page = st.Page(sections.contact.render, title='Contact', url_path='contact', icon=":material/mail:")
    cv_page = st.Page(sections.my_cv.render, title='My Resume', url_path='my_cv', icon=':material/article:')

    pages = {
        "Profile": [home_page],
        "Projects": [barnes_hut_page, cycle_gan_page],
        "Other": [contact_page, cv_page]
    }

    st.session_state["pages"] = {
        "home": home_page,
        "projects-barnes_hut": barnes_hut_page,
        "projects-cyclegan": cycle_gan_page,
        "contact": contact_page,
        "my_cv": cv_page
    }

    pg = st.navigation(pages, position="sidebar", expanded=True)
    pg.run()  # <- do not manually call your render() functions elsewhere


if __name__ == '__main__':
    main()
