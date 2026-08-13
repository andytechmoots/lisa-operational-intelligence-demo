import streamlit as st

from components.data import load_shipments
from components.ui import render_header
from examples.custody_example import classify_demo_custody


shipments = load_shipments()

render_header(
    "LISA — Custody & Responsibility Intelligence",
    "Determine who currently holds the shipment and who owns the next action.",
)


# ---------------------------------------------------------
# Preserve shipment investigation context
# ---------------------------------------------------------

waybills = shipments["waybill"].tolist()

previous_waybill = st.session_state.get(
    "selected_waybill"
)

default_index = None

if previous_waybill in waybills:
    default_index = waybills.index(
        previous_waybill
    )


waybill = st.selectbox(
    "Shipment / Waybill",
    options=waybills,
    index=default_index,
    placeholder="Select or type a waybill...",
)


if waybill is None:
    st.info(
        "Select a shipment to assess custody and responsibility."
    )
    st.stop()


st.session_state["selected_waybill"] = waybill


shipment = (
    shipments.loc[
        shipments["waybill"] == waybill
    ]
    .iloc[0]
)


# ---------------------------------------------------------
# Simplified public custody assessment
# ---------------------------------------------------------

custody_type = classify_demo_custody(
    shipment["status"]
)


if custody_type == "COMPLETED":

    current_custodian = "Delivery Completed"
    responsible_party = "None"
    required_action = "No Further Action"
    confidence = "High"

elif custody_type == "RETURN_FLOW":

    current_custodian = "Return Network"
    responsible_party = "Return Operations"
    required_action = "Monitor Return Flow"
    confidence = "Medium"

else:

    current_custodian = "Contractor Network"
    responsible_party = "Last-Mile Operations"
    required_action = "Review Shipment Progress"
    confidence = "High"


# ---------------------------------------------------------
# Shipment context
# ---------------------------------------------------------

st.subheader("Shipment Context")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Waybill",
        shipment["waybill"],
    )

with col2:
    st.metric(
        "Operational Status",
        shipment["status"]
        .replace("_", " ")
        .title(),
    )

with col3:
    st.metric(
        "Destination",
        shipment["destination"],
    )


# ---------------------------------------------------------
# Custody intelligence
# ---------------------------------------------------------

st.subheader("Custody Assessment")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Custody Type",
        custody_type.replace("_", " ").title(),
    )

with col2:
    st.metric(
        "Current Custodian",
        current_custodian,
    )

with col3:
    st.metric(
        "Confidence",
        confidence,
    )


# ---------------------------------------------------------
# Responsibility
# ---------------------------------------------------------

st.subheader("Responsibility")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Responsible Party",
        responsible_party,
    )

with col2:
    st.metric(
        "Required Action",
        required_action,
    )


# ---------------------------------------------------------
# Explainable assessment
# ---------------------------------------------------------

if custody_type == "COMPLETED":

    st.success(
        (
            f"{waybill} is delivered. "
            "Operational custody is considered complete "
            "and no further action is required."
        ),
        icon="✅",
    )

elif custody_type == "RETURN_FLOW":

    st.warning(
        (
            f"{waybill} is currently in the return flow. "
            "Return operations retain responsibility "
            "until the return lifecycle is completed."
        ),
        icon="↩️",
    )

else:

    st.info(
        (
            f"{waybill} remains within the contractor network. "
            "Last-mile operations currently own the next "
            "operational review."
        ),
        icon="📦",
    )


# ---------------------------------------------------------
# Public-demo boundary
# ---------------------------------------------------------

with st.expander(
    "About this custody assessment"
):

    st.write(
        """
        This public demonstration uses a simplified custody
        classification based on synthetic shipment states.

        The private LISA implementation uses a more detailed
        evidence-based custody and responsibility model.
        """
    )