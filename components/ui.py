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