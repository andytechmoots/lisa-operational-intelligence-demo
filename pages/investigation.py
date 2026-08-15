import streamlit as st

from components.data import load_shipments
from components.ui import (
    render_feedback,
    render_header,
)


shipments = load_shipments()


# ---------------------------------------------------------
# Available shipments
# ---------------------------------------------------------

waybills = (
    shipments["waybill"]
    .astype(str)
    .tolist()
)


# ---------------------------------------------------------
# Cross-page state
# ---------------------------------------------------------

selected_waybill = st.session_state.get(
    "selected_waybill"
)


if "_investigation_waybill" not in st.session_state:

    if selected_waybill in waybills:

        st.session_state[
            "_investigation_waybill"
        ] = selected_waybill

    else:

        st.session_state[
            "_investigation_waybill"
        ] = None


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

render_header(
    "LISA — Shipment Investigation",
    (
        "Step 2 — Understand what happened "
        "and why this shipment needs attention."
    ),
)


st.markdown(
    """
    **1. Spot what matters** ✅
    &nbsp;&nbsp;→&nbsp;&nbsp;
    **2. Investigate** 🔎
    &nbsp;&nbsp;→&nbsp;&nbsp;
    **3. Identify responsibility**
    &nbsp;&nbsp;→&nbsp;&nbsp;
    **4. Decide the next action**
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Explain guided example versus exploration
# ---------------------------------------------------------

st.info(
    (
        "**Guided example:** SYN0002 demonstrates a routing exception. "
        "You can select any synthetic shipment below to explore how "
        "LISA responds to different operational situations."
    ),
    icon="💡",
)


# ---------------------------------------------------------
# Shipment selection
# ---------------------------------------------------------

waybill = st.selectbox(
    "Explore Shipment / Waybill",
    options=waybills,
    index=None,
    placeholder="Choose or type a synthetic waybill...",
    key="_investigation_waybill",
)


if waybill is not None:

    st.session_state[
        "selected_waybill"
    ] = waybill


if waybill is None:

    st.info(
        (
            "Choose a synthetic shipment to begin. "
            "For the guided workflow, start with SYN0002."
        )
    )

    render_feedback()

    st.stop()


# ---------------------------------------------------------
# Retrieve shipment
# ---------------------------------------------------------

shipment_rows = shipments.loc[
    shipments["waybill"] == waybill
]


if shipment_rows.empty:

    st.error(
        (
            f"Shipment {waybill} could not be found "
            "in the synthetic dataset."
        )
    )

    render_feedback()

    st.stop()


shipment = shipment_rows.iloc[0]


# ---------------------------------------------------------
# Routing assessment
# ---------------------------------------------------------

is_route_exception = (
    shipment["route_status"]
    == "ROUTE_EXCEPTION"
)


if is_route_exception:

    routing_diagnosis = (
        "Routing Exception"
    )

    required_action = (
        "Review Routing"
    )


else:

    routing_diagnosis = (
        "Expected Route"
    )

    required_action = (
        "No Routing Action"
    )


# ---------------------------------------------------------
# Shipment overview
# ---------------------------------------------------------

st.subheader(
    "Shipment Overview"
)


overview_1, overview_2, overview_3, overview_4 = (
    st.columns(4)
)


with overview_1:

    st.metric(
        "Waybill",
        shipment["waybill"],
    )


with overview_2:

    st.metric(
        "Destination",
        shipment["destination"],
    )


with overview_3:

    st.metric(
        "Operational Status",
        shipment["status"]
        .replace("_", " ")
        .title(),
    )


with overview_4:

    st.metric(
        "Delivery Days",
        int(
            shipment[
                "delivery_days"
            ]
        ),
    )


# ---------------------------------------------------------
# Routing assessment
# ---------------------------------------------------------

st.subheader(
    "What happened?"
)


expected_column, arrow_column, observed_column = (
    st.columns(
        [
            1,
            0.20,
            1,
        ]
    )
)


with expected_column:

    with st.container(
        border=True
    ):

        st.caption(
            "EXPECTED LOCATION"
        )

        st.markdown(
            f"## {shipment['expected_hub']}"
        )


with arrow_column:

    st.markdown(
        (
            "<h2 style='"
            "text-align:center;"
            "padding-top:20px;"
            "'>→</h2>"
        ),
        unsafe_allow_html=True,
    )


with observed_column:

    with st.container(
        border=True
    ):

        st.caption(
            "OBSERVED LOCATION"
        )

        st.markdown(
            f"## {shipment['observed_hub']}"
        )


# ---------------------------------------------------------
# Explain result
# ---------------------------------------------------------

if is_route_exception:

    st.error(
        (
            f"{waybill} was expected at "
            f"{shipment['expected_hub']} "
            f"but was observed at "
            f"{shipment['observed_hub']}. "
            "This shipment requires operational review."
        ),
        icon="⚠️",
    )


else:

    st.success(
        (
            f"{waybill} was observed at its expected "
            f"routing location "
            f"({shipment['expected_hub']})."
        ),
        icon="✅",
    )


# ---------------------------------------------------------
# Operational assessment
# ---------------------------------------------------------

st.subheader(
    "What does LISA conclude?"
)


assessment_1, assessment_2 = (
    st.columns(2)
)


with assessment_1:

    st.metric(
        "Routing Diagnosis",
        routing_diagnosis,
    )


with assessment_2:

    st.metric(
        "Routing Action",
        required_action,
    )


# ---------------------------------------------------------
# Evidence
# ---------------------------------------------------------

with st.expander(
    "View Synthetic Shipment Evidence"
):

    evidence = (
        shipment
        .astype(str)
        .to_frame(
            name="Value"
        )
    )

    st.dataframe(
        evidence,
        width="stretch",
    )


# ---------------------------------------------------------
# Guided next step
# ---------------------------------------------------------

st.divider()


st.markdown(
    """
    <div class="next-step-box">
        <strong>
            Next question → Who owns this shipment now?
        </strong>
        <br><br>
        LISA has identified what happened.
        Continue to determine who currently owns the issue
        and what operational action should follow.
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    "### Ready for the decision?"
)


st.write(
    (
        f"We understand what happened to **{waybill}**. "
        "Now determine **who owns the issue and what "
        "should happen next.**"
    )
)


if st.button(
    (
        f"🎯 IDENTIFY RESPONSIBILITY & "
        f"NEXT ACTION — {waybill} →"
    ),
    type="primary",
    width="stretch",
):

    st.session_state[
        "selected_waybill"
    ] = waybill

    st.session_state[
        "_custody_waybill"
    ] = waybill

    st.switch_page(
        "pages/custody.py"
    )


# ---------------------------------------------------------
# Exploration guidance
# ---------------------------------------------------------

st.caption(
    (
        "Want to test a different situation? "
        "Use the shipment selector at the top of this page "
        "to investigate any other synthetic waybill."
    )
)


render_feedback()