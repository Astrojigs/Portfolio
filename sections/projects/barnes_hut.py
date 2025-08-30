import streamlit as st
from core.utils import custom_container, custom_write, chips, hero_video
from pathlib import Path
import matplotlib.pyplot as plt


# simple quadtree schematic (no external image needed)
# ————————————————————————————————————————————————————————
# Simple quadtree schematic (no external image needed)
# ————————————————————————————————————————————————————————
def draw_quadtree_schematic(levels: int = 3):
    fig, ax = plt.subplots(figsize=(4.5, 4.5))
    ax.set_aspect("equal");
    ax.axis("off")
    ax.plot([0, 1, 1, 0, 0], [1, 1, 0, 0, 1], linewidth=2)

    def subdivide(x0, y0, w, h, d):
        if d == 0: return
        xm, ym = x0 + w / 2, y0 + h / 2
        ax.plot([xm, xm], [y0, y0 + h], linewidth=1)
        ax.plot([x0, x0 + w], [ym, ym], linewidth=1)
        # show adaptivity hint by subdividing two children
        subdivide(x0, ym, w / 2, h / 2, d - 1)  # top-left
        subdivide(xm, y0, w / 2, h / 2, d - 1)  # bottom-right

    subdivide(0, 0, 1, 1, levels)
    st.pyplot(fig, clear_figure=True)


# ————————————————————————————————————————————————————————
# Tiny interactive sandboxes (teach-by-playing)
# ————————————————————————————————————————————————————————
def opening_criterion_sandbox():
    st.markdown("**Try it — Opening criterion**")
    c1, c2, c3 = st.columns(3)
    with c1:
        s = st.slider("Node size s", 0.1, 10.0, 2.0, 0.1)
    with c2:
        d = st.slider("Distance d", 0.1, 20.0, 6.0, 0.1)
    with c3:
        theta = st.slider("θ (opening angle)", 0.2, 1.2, 0.6, 0.05)

    ratio = s / d
    ok = ratio < theta
    st.latex(r"\frac{s}{d} < \theta")
    st.write(f"Computed: s/d = **{ratio:.3f}**  vs  θ = **{theta:.3f}**  →  "
             + ("✅ **approximate with the node's monopole**" if ok else "🔎 **open the node and recurse**"))
    with st.expander("What this maps to in code"):
        st.markdown(
            "- In `Quadtree.calculate_force(p)`, we set `s = max(node.w, node.h)` and `d = ||COM - p||`.\n"
            "- If `s/d < theta`: use the node’s **mass at COM** (single interaction).\n"
            "- Else: **descend** into children and sum their contributions."
        )


def softening_sandbox():
    st.markdown("**Try it — Softened gravity**")
    c1, c2, c3, c4 = st.columns(4)
    with c1: m1 = st.number_input("m₁", 0.1, 1000.0, 1.0, 0.1)
    with c2: m2 = st.number_input("m₂", 0.1, 1000.0, 1.0, 0.1)
    with c3: r = st.slider("separation r", 0.05, 5.0, 0.5, 0.05)
    with c4: eps = st.slider("softening ε", 0.0, 1.0, 0.15, 0.01)
    G = st.number_input("G (sim units)", 0.0001, 10.0, 0.1, 0.01)

    # Newton vs Plummer-softened magnitudes
    F_newton = G * m1 * m2 / (r * r)
    F_soft = G * m1 * m2 / ((r * r + eps * eps) ** 1.5) * r  # |F| = G m1 m2 r / (r^2+ε^2)^{3/2}
    st.latex(r"\mathbf{F} = -\,G\,m_1 m_2\,\frac{\mathbf{r}}{(r^2+\varepsilon^2)^{3/2}}")
    st.write(f"|F| (Newton, no ε) ≈ **{F_newton:.4f}**  |  "
             f"|F| (softened) ≈ **{F_soft:.4f}**")
    st.caption(
        "As ε→0 the softened force → Newtonian. ε>0 tames huge forces at very small r (prevents numerical blow-ups).")


def render():
    custom_write("Barnes–Hut N-Body (2D)", type="h1")
    st.caption("From data structures → forces → leapfrog → spinning disk galaxy")
    chips(["O(N log N) gravity", "Quadtree", "Softening", "Leapfrog (KDK)"])

    # Intro tabs: Intuition | Equations explained
    t_overview, t_equations = st.tabs(["Overview", "Equations explained"])
    with t_overview:
        st.markdown(
            "Computing all pairwise gravitational forces is **O(N²)**. "
            "Barnes–Hut speeds this up by grouping far-away particles: if a node looks small "
            "from a particle, we approximate that entire node with **one mass at its center of mass (COM)**."
        )
        c1, c2 = st.columns([1, 1])
        with c1:
            custom_write("Quadtree in one picture", type="h3")
            draw_quadtree_schematic()
        with c2:
            custom_write("Complexity drop", type="h3")
            st.markdown(
                "- Building the tree: roughly **O(N log N)**\n"
                "- Force evaluation: most far-away nodes pass the opening test → **~O(N log N)** total\n"
                "- Accuracy knob: θ ↓ ⇒ more opens (slower, more accurate); θ ↑ ⇒ fewer opens"
            )

    with t_equations:
        # Opening criterion
        with custom_container(key="open-criterion"):
            custom_write("Opening test (when can a node stand in for many bodies?)", type="h3")
            st.latex(r"\frac{s}{d} < \theta")
            st.markdown(
                "- **s**: node side length (use the larger of width/height)\n"
                "- **d**: distance from particle to the node’s COM\n"
                "- **θ**: threshold (~0.5–0.8)"
            )
            opening_criterion_sandbox()

        # Softened gravity
        with custom_container(key="softening"):
            custom_write("Softened gravity (avoid singular accelerations)", type="h3")
            st.latex(r"\mathbf{F}_i=-G\,m_i\sum_{j\ne i} m_j\frac{\mathbf{r}_{ij}}{(r_{ij}^2+\varepsilon^2)^{3/2}}")
            st.markdown(
                "Replacing $r^2$ with $r^2+\\varepsilon^2$ damps forces at tiny separations. "
                "This keeps the integration stable without needing tiny time-steps."
            )
            softening_sandbox()

        # Leapfrog KDK
        with custom_container(key="leapfrog"):
            custom_write("Leapfrog (KDK) integrator (energy-friendly)", type="h3")
            st.latex(r"v^{n+\frac12}=v^n+\frac{\Delta t}{2}\,a(x^n)")
            st.latex(r"x^{n+1}=x^n+\Delta t\,v^{n+\frac12}")
            st.latex(r"v^{n+1}=v^{n+\frac12}+\frac{\Delta t}{2}\,a(x^{n+1})")
            st.markdown(
                "Half-kick → drift → rebuild tree and recompute $a(x^{n+1})$ → half-kick. "
                "Symplectic structure keeps long-term energy drift bounded."
            )

    # Architecture / file tour
    custom_write("What each class/method does (from my OOP file)", type="h2")
    with custom_container(key="file-tour"):
        # Point
        custom_write("Point", type="h3")
        st.markdown("- Particle state: `x, y, vx, vy, mass, color`.")
        # Rectangle
        custom_write("Rectangle", type="h3")
        st.markdown("- Node box with `contains(p)` (inclusive edges) and `draw(ax)` for debugging.")
        # Quadtree
        custom_write("Quadtree", type="h3")
        st.markdown(
            "- **State**: `boundary`, `mass`, `comx`, `comy`, `children[4]`, `points`, `divided`.\n"
            "- **Invariant**: every node stores the **total mass** and **COM** of its subtree (updated **incrementally** during `insert`).\n"
            "- **Public API**:\n"
            "  - `insert(p)`: route point → maybe subdivide → push down; update mass/COM on the way.\n"
            "  - `calculate_force(p)`: leaf = exact sum; internal = opening test → either monopole or recurse.\n"
            "  - `draw(ax)`: visualize bounds."
        )
        # Utilities & driver
        custom_write("Utilities & driver", type="h3")
        st.markdown(
            "- `_make_square_bounds(points)`: padded square root so the tree encloses the system.\n"
            "- `_compute_accelerations(points, tree)`: call `calculate_force` for each point → arrays of ax, ay.\n"
            "- `barnes_hut_sim(...)`: **KDK loop**: half-kick → drift → rebuild tree → new `a` → half-kick."
        )

    # ICs
    custom_write("Initial conditions: exponential disk + bulge", type="h2")
    st.markdown("Disk surface density and induced radial PDF:")
    st.latex(r"\Sigma(r) \propto e^{-r/R_d} \;\Rightarrow\; p(r) \propto r\,e^{-r/R_d}")
    st.markdown("Sampling trick (Erlang, k=2) and the exponential prior:")
    st.latex(r"r = R_d\,(E_1 + E_2), \qquad E_k \sim \mathrm{Exp}(1)")
    st.markdown("Rotation curve used for near-circular initial speeds:")
    st.latex(r"v_{\mathrm{circ}}(r) = \sqrt{\dfrac{G\,M(<r)}{\max(r, r_{\min})}}")
    st.caption("Clamp with $r_{\\min}$ (e.g., 0.5) to avoid a singular center; then add a small velocity dispersion.")

    with st.expander("Code: make_exponential_disk"):
        st.code(
            r'''def make_exponential_disk(
                n_total: int = 400,
                R_d: float = 8.0,
                R_max: float = 40.0,
                M_total: float = 400.0,
                G_used: float = 0.1,
                bulge_frac: float = 0.15,
                bulge_sigma: float = 2.0,
                rot_sign: int = +1,
                v_disp: float = 0.05,
                seed: int = 7,
            ) -> list[Point]:
                import numpy as np
                rng = np.random.default_rng(seed)
                n_bulge = int(bulge_frac * n_total)
                n_disk  = n_total - n_bulge
                m = M_total / n_total
                pts: list[Point] = []
                # Bulge
                if n_bulge > 0:
                    xb = rng.normal(0.0, bulge_sigma, size=n_bulge)
                    yb = rng.normal(0.0, bulge_sigma, size=n_bulge)
                    vxb = rng.normal(0.0, v_disp, size=n_bulge)
                    vyb = rng.normal(0.0, v_disp, size=n_bulge)
                    for i in range(n_bulge):
                        pts.append(Point(float(xb[i]), float(yb[i]), mass=m, vx=float(vxb[i]), vy=float(vyb[i])))
                # Disk radii via Erlang (k=2)
                e1 = rng.exponential(1.0, size=n_disk); e2 = rng.exponential(1.0, size=n_disk)
                r  = np.clip(R_d * (e1 + e2), 0.0, R_max)
                th = rng.uniform(0, 2*np.pi, size=n_disk)
                xd, yd = r*np.cos(th), r*np.sin(th)
                # Enclosed mass (disk + cored bulge)
                M_disk  = M_total * (1.0 - bulge_frac)
                M_bulge = M_total * bulge_frac
                a = 2.5 * bulge_sigma + 1e-6
                M_enc = M_disk * (1.0 - np.exp(-r/R_d)*(1.0 + r/R_d)) + M_bulge * (r**2/(r**2 + a**2))
                # Tangential velocity + small dispersion
                v_c = np.sqrt(np.maximum(0.0, G_used * M_enc / np.maximum(r, 0.5)))
                tx, ty = rot_sign * (-np.sin(th)), rot_sign * (np.cos(th))
                vxd = v_c * tx + rng.normal(0.0, v_disp, size=n_disk)
                vyd = v_c * ty + rng.normal(0.0, v_disp, size=n_disk)
                for i in range(n_disk):
                    pts.append(Point(float(xd[i]), float(yd[i]), mass=m, vx=float(vxd[i]), vy=float(vyd[i])))
                return pts
            ''', language="python")

    # How I run it
    custom_write("Run settings I used", type="h2")
    st.code(
        r'''G_sim = 0.1
        pts = make_exponential_disk(
            n_total=360, R_d=7.0, R_max=35.0, M_total=360.0, G_used=G_sim,
            bulge_frac=0.18, bulge_sigma=2.0, rot_sign=+1, v_disp=0.08, seed=42,
        )
        barnes_hut_sim(
            pts,
            dt=0.06, G=G_sim, theta=0.6, eps=0.15,
            capacity=1, max_depth=32,
            n_frames=640, draw_quadtree=False,
            fixed_viewport=(-45,45,-45,45),
            # save_to_video="./core/references/Project Files/Barnes-Hut/ep2_web.mp4",
            video_fps=30
        )
        ''', language="python")

    # Result videos
    custom_write("Results (videos)", type="h2")
    with custom_container(key="Barnes-Hut Example"):
        c1, c2 = st.columns([1, 1])
        with c1:
            hero_video("./core/references/Project Files/Barnes-Hut/ep2_web.mp4",
                       mp4_path="./core/references/Project Files/Barnes-Hut/ep2_web.mp4")
        with c2:
            hero_video('./core/references/Project Files/Barnes-Hut/ep2_quadtree_web.mp4',
                       mp4_path="./core/references/Project Files/Barnes-Hut/ep2_quadtree_web.mp4")

    # ————————————————————————————————————————————————————————————————
    # 6) Tuning & gotchas
    # ————————————————————————————————————————————————————————————————

    c1, c2 = st.columns(2)
    with c1:
        custom_write("Tuning & gotchas", type="h2")
        st.markdown(
            "- **θ (opening angle)**: smaller → more accurate, slower. Try 0.5–0.8.\n"
            "- **ε (softening)**: prevents singular forces; too small → noisy core, too large → overly fluffy.\n"
            "- **capacity / max_depth**: guard against deep trees with overlapping points.\n"
            "- **Energy behaviour**: leapfrog (KDK) keeps energy drift bounded compared to Euler.\n"
            "- **Video export**: share H.264/yuv420p with `+faststart` (your `_web.mp4` files)."
        )

        custom_write("Source", type="h2")
        st.markdown(
            "- Full OOP implementation in my repo: "
            "[Orbital-simulations/barnes_hut.py](https://github.com/Astrojigs/Orbital-simulations/b"
            "lob/main/barnes_hut.py)\n"
            "- This page documents the architecture and reproduces the notebook example."
        )
    with c2:
        with custom_container(key="2nd Barnes Hut example"):
            custom_write("Barnes-Hut Algorithm in action (Example 2)", color="gray", type="h5")
            hero_video('./core/references/Project Files/Barnes-Hut/ep1_web.mp4',
                       mp4_path="./core/references/Project Files/Barnes-Hut/ep1_web.mp4", max_width_px=400)
    # custom_write("<i>More details coming in soon</i>...", color='gray')
