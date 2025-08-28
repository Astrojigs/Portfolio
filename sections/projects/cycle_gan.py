# sections/projects/cycle_gan.py
from __future__ import annotations

import streamlit as st
from core.utils import custom_container, chips

TITLE = "Aerial Images → Maps (CycleGAN)"
SUB = "Unpaired image-to-image translation for cartographic rendering"

# --- Repo assets (raw GitHub so Streamlit can display them) ---
IMG_AERIAL = "https://github.com/Astrojigs/Aerial-images-to-maps/raw/main/Images/example%20image%20aerial%20-%20Copy.jpg"
IMG_MAP    = "https://github.com/Astrojigs/Aerial-images-to-maps/raw/main/Images/example%20image%20map%20-%20Copy.jpg"
IMG_MODEL  = "https://github.com/Astrojigs/Aerial-images-to-maps/raw/main/model.png"

URL_REPO   = "https://github.com/Astrojigs/Aerial-images-to-maps"
URL_GEN    = "https://github.com/Astrojigs/Aerial-images-to-maps/blob/main/Generator_arc.py"
URL_DISC   = "https://github.com/Astrojigs/Aerial-images-to-maps/blob/main/Discriminator_arc.py"
URL_LOSSES = "https://github.com/Astrojigs/Aerial-images-to-maps/blob/main/losses.py"
URL_NOTE   = "https://github.com/Astrojigs/Aerial-images-to-maps/blob/main/Evaluation%20of%20cycle-GAN.ipynb"


def _hero():
    st.title(TITLE)
    st.caption(SUB)
    chips(
        [
            {"label": "Python", "variant": "line"},
            {"label": "PyTorch", "variant": "info", "icon": "🔥"},
            {"label": "CycleGAN", "variant": "warn"},
            {"label": "Satellite", "variant": "line"},
            {"label": "Image2Image", "variant": "info"},
        ],
        size="sm",
    )

    with custom_container(key="cyclegan-hero", bg="#0b1020", text_color="#f5f7ff",
                          accent="#7bd389", accent_width="6px",
                          elevation=2, hover_elevation=3, padding="20px"):
        st.subheader("What this project does")
        st.write(
            "Translate **aerial/satellite tiles → minimalist map renderings** without paired supervision "
            "(CycleGAN). The system learns two mappings, **G: aerial→map** and **F: map→aerial**, "
            "regularized by **cycle-consistency** and **identity** losses to preserve structure and style."
        )

        c1, c2 = st.columns(2, vertical_alignment="center")
        with c1:
            st.image(IMG_AERIAL, caption="Input aerial tile (128×128 / 256×256)", use_container_width=True)
        with c2:
            st.image(IMG_MAP, caption="Generated map-style rendering", use_container_width=True)

        st.markdown(
            f"↗ **Repo:** [{URL_REPO}]({URL_REPO}) &nbsp;&nbsp; "
            f"•  **Eval notebook:** [{URL_NOTE.split('/')[-1]}]({URL_NOTE})"
        )


def _architecture():
    with custom_container(key="cyclegan-arch", bg="#ffffff", accent="#FF8C00",
                          elevation=2, hover_elevation=4, padding="18px"):
        st.subheader("Architecture")
        st.write(
            "- Two **generators** (G: X→Y, F: Y→X) and two **discriminators** (D_Y, D_X).\n"
            "- G and F learn inverse style mappings; D_X and D_Y enforce realism in each domain.\n"
            "- Implementations for generator/discriminator are in your repo (links below)."
        )

        # Model overview diagram
        st.image(IMG_MODEL, caption="CycleGAN overview used in this project", use_container_width=True)

        c1, c2, c3 = st.columns([1, 1, 1])
        with c1: st.page_link(URL_GEN, label="🧬 Generator code (G/F)", icon=":material/developer_guide:")
        with c2: st.page_link(URL_DISC, label="🪄 Discriminator code (D_X / D_Y)", icon=":material/visibility:")
        with c3: st.page_link(URL_LOSSES, label="🧪 Loss functions (PyTorch)", icon=":material/function:")


def _math():
    with custom_container(key="cyclegan-math", bg="#ffffff", elevation=2, hover_elevation=3, padding="18px"):
        st.subheader("Objective functions (math)")

        st.markdown("**Adversarial loss (for X→Y):**")
        st.latex(r"""
        \mathcal{L}_{\mathrm{GAN}}(G, D_Y, X, Y)
        = \mathbb{E}_{y \sim p_{\mathrm{data}}(Y)}[\log D_Y(y)]
        + \mathbb{E}_{x \sim p_{\mathrm{data}}(X)}[\log(1 - D_Y(G(x)))]\,.
        """)

        st.markdown("**Adversarial loss (for Y→X):**")
        st.latex(r"""
        \mathcal{L}_{\mathrm{GAN}}(F, D_X, Y, X)
        = \mathbb{E}_{x \sim p_{\mathrm{data}}(X)}[\log D_X(x)]
        + \mathbb{E}_{y \sim p_{\mathrm{data}}(Y)}[\log(1 - D_X(F(y)))]\,.
        """)

        st.markdown("**Cycle-consistency loss:**")
        st.latex(r"""
        \mathcal{L}_{\mathrm{cyc}}(G, F) =
        \mathbb{E}_{x \sim p(X)}\left[\lVert F(G(x)) - x \rVert_1\right]
        + \mathbb{E}_{y \sim p(Y)}\left[\lVert G(F(y)) - y \rVert_1\right].
        """)

        st.markdown("**Identity loss (style preservation):**")
        st.latex(r"""
        \mathcal{L}_{\mathrm{id}}(G, F) =
        \mathbb{E}_{y \sim p(Y)}\left[\lVert G(y) - y \rVert_1\right]
        + \mathbb{E}_{x \sim p(X)}\left[\lVert F(x) - x \rVert_1\right].
        """)

        st.markdown("**Full objective:**")
        st.latex(r"""
        \min_{G,F}\max_{D_X,D_Y}\;
        \mathcal{L} =
        \mathcal{L}_{\mathrm{GAN}}(G,D_Y,X,Y)
        + \mathcal{L}_{\mathrm{GAN}}(F,D_X,Y,X)
        + \lambda_{\mathrm{cyc}}\mathcal{L}_{\mathrm{cyc}}(G,F)
        + \lambda_{\mathrm{id}}\mathcal{L}_{\mathrm{id}}(G,F).
        """)

        st.caption(
            "λ terms balance realism vs. structure/style preservation. See the evaluation notebook for the "
            "exact settings used during experimentation."
        )


def _data_training():
    with custom_container(key="cyclegan-data", bg="#fbfaf7", elevation=1, hover_elevation=2, padding="18px"):
        st.subheader("Dataset & training")
        st.markdown(
            "- **Tiles:** trained/evaluated on **128×128** and **256×256** patches (see notebook for runs).\n"
            "- **Preprocessing:** standard normalization; domain batches sampled independently.\n"
            "- **Optimization:** adversarial training with cycle/identity regularization.\n"
            "- **Repro:** all code + notebook are in the repo; re-run end-to-end with your GPU."
        )
        st.page_link(URL_NOTE, label="📓 Open evaluation notebook", icon=":material/description:")


def _examples():
    with custom_container(key="cyclegan-examples", bg="#ffffff", elevation=2, hover_elevation=4, padding="18px"):
        st.subheader("Examples")
        st.write("A few qualitative examples taken directly from the repository images:")

        c1, c2 = st.columns(2)
        with c1:
            st.image(IMG_AERIAL, caption="Aerial (input)", use_container_width=True)
        with c2:
            st.image(IMG_MAP, caption="Map-style (G(x))", use_container_width=True)

        st.caption("More results and ablations are included in the notebook and codebase.")


def render():
    _hero()
    _architecture()
    _math()
    _data_training()
    _examples()
