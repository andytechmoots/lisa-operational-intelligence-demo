import streamlit as st


def render_header(
    title: str,
    subtitle: str,
) -> None:
    st.title(title)

    st.caption(subtitle)

    st.info(
        "SYNTHETIC DEMO — No customer or production data.",
        icon="🧪",
    )


def render_feedback() -> None:
    st.divider()

    st.subheader("Help improve LISA")
    st.caption(
        "Explored the demo? Share a quick 2-minute feedback to help shape future iterations."
    )

    st.link_button(
        "💬 Give Feedback",
        "https://forms.gle/3R27EMmUa7gcWNW96",
        help="Open the LISA Demo feedback form.",
    )