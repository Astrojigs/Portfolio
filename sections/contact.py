# sections/contact.py
import streamlit as st
from urllib.parse import quote_plus
from st_social_media_links import SocialMediaIcons
from core.utils import custom_write, chips, custom_container, center_gif
from urllib.parse import urlencode, quote


def _mailto(to: str, subject: str, body: str, cc: str | None = None, bcc: str | None = None) -> str:
    """
    Build a robust mailto: link (uses CRLF for newlines so Outlook/Apple Mail/Gmail parse body correctly).
    """
    # Gmail/Outlook prefer CRLF
    body = (body or "").replace("\n", "\r\n")
    params = {"subject": subject or "", "body": body}
    if cc: params["cc"] = cc
    if bcc: params["bcc"] = bcc
    # url encode with quote (spaces => %20) is more consistent than quote_plus for some handlers
    return f"mailto:{to}?{urlencode(params, quote_via=quote)}"


def _gmail_compose(to: str, subject: str, body: str, cc: str | None = None, bcc: str | None = None) -> str:
    """
    Web Gmail fallback (opens a new compose window with fields prefilled).
    """
    q = {
        "view": "cm", "fs": "1",
        "to": to, "su": subject or "", "body": body or ""
    }
    if cc: q["cc"] = cc
    if bcc: q["bcc"] = bcc
    return f"https://mail.google.com/mail/?{urlencode(q, quote_via=quote)}"


EMAIL_TO = "astrojis24@gmail.com"  # ← change this to your email
LINKEDIN = "https://www.linkedin.com/in/astrojigs"  # ← update
GITHUB = "https://github.com/Astrojigs"


def render():
    custom_write("Get In Touch", type="h1", align="center", color='gray')
    custom_write(
        "I work at the intersection of data, Python, and clear storytelling.<br> "
        "Whether you’re hiring, exploring a collaboration, or want feedback on an idea, "
        "I’d love to hear from you.",
        type="h5", align="center", color='gray'
    )

    # What I'm open to
    chips(
        [
            {"label": "roles", "icon": "💼", "variant": "alt"},
            {"label": "Streamlit dashboards", "icon": "📊"},
            {"label": "ETL / SQL work", "icon": "🛠"},
            {"label": "AI/ML", "icon": "🤖"},
            {"label": "Coffee chat (Dublin/remote)", "icon": "☕"},
        ],
        size="sm"
    )

    # Quick links
    with custom_container(key="contact-links", bg="#fff", elevation=1, padding="16px 18px"):
        left, right = st.columns([1, 1])
        with left:
            # --- Contact card (avatar + title + local time) ---
            from datetime import datetime
            from zoneinfo import ZoneInfo

            avatar_path = "./core/references/images/ProfilePic.jpeg"  # adjust if needed
            now_dublin = datetime.now(ZoneInfo("Europe/Dublin")).strftime("%a, %d %b · %H:%M")

            card = st.container()
            with card:
                a, b = st.columns([0.38, 0.62], vertical_alignment="center")
                with a:
                    st.image(avatar_path, use_container_width=True)
                with b:
                    st.markdown("### Jigar Patel")
                    st.markdown("Data Analyst · Python Developer")
                    st.caption(f"📍 Dublin · {now_dublin} (local)")
                    # Internal resume link (keeps your existing route)
                    st.page_link(st.session_state['pages']['my_cv'], label="📄 View Resume",
                                 icon=":material/description:")

            st.divider()

            # --- Social links (keeps your library) ---
            st.markdown("**Connect**")
            social_media_links = [
                "https://www.github.com/astrojigs",
                "https://www.linkedin.com/in/astrojigs/",
            ]
            SocialMediaIcons(social_media_links).render()
            st.divider()
            # --- Save contact (vCard download) ---
            vcard = """BEGIN:VCARD
        VERSION:3.0
        N:Patel;Jigar;;;
        FN:Jigar Patel
        TITLE:Data Analyst / Python Developer
        EMAIL;TYPE=INTERNET;TYPE=WORK:astrojis24@gmail.com
        URL:https://astrojigs.dev
        URL:https://github.com/Astrojigs
        URL:https://www.linkedin.com/in/astrojigs
        ADR;TYPE=WORK:;;Dublin;;;Ireland
        END:VCARD
        """
            st.download_button("💾 Save contact (vCard)", vcard, file_name="Jigar_Patel.vcf", mime="text/vcard")

            st.caption("Prefer LinkedIn? Connect and mention you came via the website so I don’t miss it.")


        with right:
            with st.form("contact_form", clear_on_submit=False):
                st.write("#### Send your message")
                name = st.text_input("Your name")
                reply_to = st.text_input("Your email")
                msg = st.text_area("Message", height=140, placeholder="Tell me a bit about the role, project, or idea…")
                submitted = st.form_submit_button("Compose email draft", type='primary')
                if submitted:
                    subject = f"Portfolio contact from {name or 'someone'}"
                    body_lines = [
                        f"Name: {name or ''}",
                        f"Email: {reply_to or ''}",
                        "",
                        msg or "",
                    ]
                    body = "\n".join(body_lines)

                    mailto = _mailto(EMAIL_TO, subject, body)
                    gmail = _gmail_compose(EMAIL_TO, subject, body)

                    st.success("Choose how you'd like to send your message:")
                    st.markdown(
                        f"""
                        <div style="display:flex; gap:10px; flex-wrap:wrap;">
                          <a href="{mailto}" class="st-emotion-cache-link" target="_blank" rel="noopener"
                             style="text-decoration:none; padding:8px 12px; border-radius:8px; border:1px solid #bbb;">
                             📧 Open in Mail app
                          </a>
                          <a href="{gmail}" class="st-emotion-cache-link" target="_blank" rel="noopener"
                             style="text-decoration:none; padding:8px 12px; border-radius:8px; border:1px solid #bbb;">
                             ✉️ Open in Gmail
                          </a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.caption("Tip: If the Mail app opens blank, your OS may not have a default mail handler set. "
                               "On Windows: Settings → Apps → Default apps → Email.")

    # Optional: small note on response time / availability
    custom_write("I usually reply within 24–48 hours. If it’s urgent, please mention it in the subject line."
                 "<br><br><br>",
                 type='caption')
