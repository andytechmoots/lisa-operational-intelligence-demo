import streamlit as st

from components.data import load_shipments
from components.ui import render_header


shipments = load_shipments()

render_header(
    "LISA — Shipment & Exception Investigation",
    "Investigate routing, operational state and required intervention.",
)


# ---------------------------------------------------------
# Shipment search
# ---------------------------------------------------------

waybill = st.selectbox(
    "Search Shipment / Waybill",
    options=shipments["waybill"].tolist(),
    index=None,
    placeholder="Select or type a waybill...",
)

if waybill is not None:
    st.session_state["selected_waybill"] = waybill


if waybill is None:
    st.info(
        "Search for a synthetic waybill to begin an investigation."
    )
    st.stop()


shipment = (
    shipments.loc[
        shipments["waybill"] == waybill
    ]
    .iloc[0]
)


# ---------------------------------------------------------
# Derive simplified public-demo assessment
# ---------------------------------------------------------

is_route_exception = (
    shipment["route_status"]
    == "ROUTE_EXCEPTION"
)

if is_route_exception:
    routing_diagnosis = "Routing Exception"
    required_action = "Review Routing"
else:
    routing_diagnosis = "Expected Route"
    required_action = "No Routing Action"


# ---------------------------------------------------------
# Shipment overview
# ---------------------------------------------------------

st.subheader("Shipment Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Waybill",
        shipment["waybill"],
    )

with col2:
    st.metric(
        "Destination",
        shipment["destination"],
    )

with col3:
    st.metric(
        "Operational Status",
        shipment["status"].replace("_", " ").title(),
    )

with col4:
    st.metric(
        "Delivery Days",
        int(shipment["delivery_days"]),
    )


# ---------------------------------------------------------
# Routing assessment
# ---------------------------------------------------------

st.subheader("Routing Assessment")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Expected Hub",
        shipment["expected_hub"],
    )

with col2:
    st.metric(
        "Observed Hub",
        shipment["observed_hub"],
    )

with col3:
    st.metric(
        "Routing Outcome",
        routing_diagnosis,
    )


# ---------------------------------------------------------
# Explain result
# ---------------------------------------------------------

if is_route_exception:

    st.error(
        (
            f"{waybill} was expected at "
            f"{shipment['expected_hub']} but was observed at "
            f"{shipment['observed_hub']}."
        ),
        icon="⚠️",
    )

else:

    st.success(
        (
            f"{waybill} was observed at its expected "
            f"routing location ({shipment['expected_hub']})."
        ),
        icon="✅",
    )


# ---------------------------------------------------------
# Responsibility / action
# ---------------------------------------------------------

st.subheader("Operational Assessment")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Routing Diagnosis",
        routing_diagnosis,
    )

with col2:
    st.metric(
        "Required Action",
        required_action,
    )


# ---------------------------------------------------------
# Raw synthetic evidence
# ---------------------------------------------------------

with st.expander("View Synthetic Shipment Evidence"):

    st.dataframe(
        shipment.to_frame(
            name="Value"
        ),
        use_container_width=True,
    )