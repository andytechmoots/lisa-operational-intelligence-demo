import streamlit as st


st.set_page_config(
    page_title="LISA",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


operations_page = st.Page(
    "pages/operations.py",
    title="Operations Command Centre",
    icon="📊",
    default=True,
)

investigation_page = st.Page(
    "pages/investigation.py",
    title="Shipment Investigation",
    icon="🔎",
)

custody_page = st.Page(
    "pages/custody.py",
    title="Custody & Responsibility",
    icon="🧭",
)


navigation = st.navigation(
    [
        operations_page,
        investigation_page,
        custody_page,
    ],
    position="top",
)

navigation.run()