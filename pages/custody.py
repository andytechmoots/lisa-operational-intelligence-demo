import streamlit as st

from components.data import load_shipments
from components.ui import (
    render_feedback,
    render_header,
)
from examples.custody_example import (
    classify_demo_custody,
)


shipments = load_shipments()


# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def clear_custody_selection() -> None:
    st.session_state["selected_waybill"] = None
    st.session_state["_custody_waybill"] = None


# ---------------------------------------------------------
# Page header
# ---------------------------------------------------------

render_header(
    "LISA — Responsibility & Action",
    (
        "Step 3 — Identify who owns the shipment. "
        "Step 4 — Decide the next operational action."
    ),
)


st.markdown(
    """
    **1. Spot what matters** ✅
    &nbsp;&nbsp;→&nbsp;&nbsp;
    **2. Investigate** ✅
    &nbsp;&nbsp;→&nbsp;&nbsp;
    **3. Identify responsibility** ✅
    &nbsp;&nbsp;→&nbsp;&nbsp;
    **4. Decide the next action** 🎯
    """,
    unsafe_allow_html=True,
)


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


if "_custody_waybill" not in st.session_state:

    if selected_waybill in waybills:
        st.session_state[
            "_custody_waybill"
        ] = selected_waybill

    else:
        st.session_state[
            "_custody_waybill"
        ] = None


# ---------------------------------------------------------
# Exploration guidance
# ---------------------------------------------------------

st.info(
    (
        "**SYN0002 is the guided example.** "
        "You can select any synthetic shipment below to compare "
        "different responsibility and action outcomes."
    ),
    icon="💡",
)


# ---------------------------------------------------------
# Shipment selector
# ---------------------------------------------------------

waybill = st.selectbox(
    "Explore Shipment / Waybill",
    options=waybills,
    index=None,
    placeholder="Choose a synthetic shipment...",
    key="_custody_waybill",
)


if waybill is not None:
    st.session_state[
        "selected_waybill"
    ] = waybill


if waybill is None:

    st.info(
        (
            "Choose a shipment to assess "
            "responsibility and next action."
        )
    )

    render_feedback()
    st.stop()


# ---------------------------------------------------------
# Retrieve selected shipment
# ---------------------------------------------------------

shipment_rows = shipments.loc[
    shipments["waybill"] == waybill
]


if shipment_rows.empty:

    st.error(
        (
            f"Shipment {waybill} could not be found "
            "in the synthetic demonstration dataset."
        )
    )

    render_feedback()
    st.stop()


shipment = shipment_rows.iloc[0]


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


elif custody_type == "RETURN_FLOW":

    current_custodian = "Return Network"
    responsible_party = "Return Operations"
    required_action = "Monitor Return Flow"


else:

    current_custodian = "Contractor Network"
    responsible_party = "Last-Mile Operations"
    required_action = "Review Shipment Progress"


# ---------------------------------------------------------
# Shipment context
# ---------------------------------------------------------

st.subheader(
    "Shipment Context"
)


context_1, context_2, context_3 = (
    st.columns(3)
)


with context_1:

    st.metric(
        "Waybill",
        shipment["waybill"],
    )


with context_2:

    st.metric(
        "Operational Status",
        shipment["status"]
        .replace("_", " ")
        .title(),
    )


with context_3:

    st.metric(
        "Destination",
        shipment["destination"],
    )


# ---------------------------------------------------------
# Common routing context
# ---------------------------------------------------------

expected_hub = str(
    shipment["expected_hub"]
)

observed_hub = str(
    shipment["observed_hub"]
)

route_exception = (
    expected_hub != observed_hub
)


# ---------------------------------------------------------
# LISA operational decision
# ---------------------------------------------------------

st.subheader(
    "🎯 LISA Operational Decision"
)


# =========================================================
# COMPLETED
# =========================================================

if custody_type == "COMPLETED":

    st.success(
        f"✅ **{waybill} — No operational action required**"
    )


    decision_1, decision_2, decision_3 = (
        st.columns(3)
    )


    with decision_1:

        st.markdown(
            """
            #### ✅ What happened?
            """
        )

        st.markdown(
            """
            **Outcome**
            Delivered
            """
        )


    with decision_2:

        st.markdown(
            """
            #### 🧭 Who owns it?
            """
        )

        st.markdown(
            f"""
            **Current Ownership**
            {current_custodian}

            **Responsible Team**
            {responsible_party}
            """
        )


    with decision_3:

        st.markdown(
            """
            #### 🎯 What happens next?
            """
        )

        st.markdown(
            f"""
            **Next Action**
            {required_action}
            """
        )


    st.markdown(
        "### Recommended Operational Action"
    )

    st.success(
        "✅ **No Further Action — Shipment Completed**"
    )


# =========================================================
# RETURN FLOW
# =========================================================

elif custody_type == "RETURN_FLOW":

    st.warning(
        f"↩️ **{waybill} — Return flow requires monitoring**"
    )


    decision_1, decision_2, decision_3 = (
        st.columns(3)
    )


    with decision_1:

        st.markdown(
            """
            #### ↩️ What happened?
            """
        )

        st.markdown(
            f"""
            **Operational State**
            Return Flow

            **Current Status**
            {shipment["status"].replace("_", " ").title()}
            """
        )


    with decision_2:

        st.markdown(
            """
            #### 🧭 Who owns it?
            """
        )

        st.markdown(
            f"""
            **Current Ownership**
            {current_custodian}

            **Responsible Team**
            {responsible_party}
            """
        )


    with decision_3:

        st.markdown(
            """
            #### 🎯 What happens next?
            """
        )

        st.markdown(
            f"""
            **Next Action**
            {required_action}
            """
        )


    st.markdown(
        "### Recommended Operational Action"
    )

    st.warning(
        (
            f"↩️ **{required_action}** — "
            f"Assigned to **{responsible_party}**"
        )
    )


# =========================================================
# ACTIVE / CONTRACTOR
# =========================================================

else:

    st.error(
        f"🎯 **{waybill} — Operational attention required**"
    )


    decision_1, decision_2, decision_3 = (
        st.columns(3)
    )


    with decision_1:

        st.markdown(
            """
            #### ⚠️ What happened?
            """
        )

        if route_exception:

            st.markdown(
                f"""
                **Problem**
                Routing Exception

                **Expected Hub**
                {expected_hub}

                **Observed Hub**
                {observed_hub}
                """
            )

        else:

            st.markdown(
                f"""
                **Problem**
                Shipment Progress Review

                **Current Status**
                {shipment["status"].replace("_", " ").title()}
                """
            )


    with decision_2:

        st.markdown(
            """
            #### 🧭 Who owns it?
            """
        )

        st.markdown(
            f"""
            **Current Ownership**
            {current_custodian}

            **Responsible Team**
            {responsible_party}
            """
        )


    with decision_3:

        st.markdown(
            """
            #### 🎯 What happens next?
            """
        )

        st.markdown(
            f"""
            **Next Action**
            {required_action}
            """
        )


    st.markdown(
        "### Recommended Operational Action"
    )

    st.success(
        (
            f"🎯 **{required_action}** — "
            f"Assigned to **{responsible_party}**"
        )
    )


# ---------------------------------------------------------
# Value explanation
# ---------------------------------------------------------

st.caption(
    (
        "LISA connects the operational signal with shipment context "
        "to identify ownership and the recommended next action."
    )
)


if custody_type == "COMPLETED":

    st.info(
        (
            "LISA recognizes that this shipment no longer requires "
            "intervention, allowing operations teams to focus attention "
            "on active exceptions."
        ),
        icon="💡",
    )


elif custody_type == "RETURN_FLOW":

    st.info(
        (
            "LISA recognizes that the shipment has moved into a "
            "different operational workflow and directs responsibility "
            "toward Return Operations."
        ),
        icon="💡",
    )


else:

    st.info(
        (
            "Instead of manually reconstructing the shipment history "
            "and deciding which team should investigate, LISA connects "
            "the operational signal with ownership and surfaces "
            "the next action."
        ),
        icon="💡",
    )


# ---------------------------------------------------------
# Supporting assessment detail
# ---------------------------------------------------------

with st.expander(
    "View assessment details"
):

    st.subheader(
        "Custody Assessment"
    )


    custody_1, custody_2 = (
        st.columns(2)
    )


    with custody_1:

        st.metric(
            "Custody Type",
            custody_type
            .replace("_", " ")
            .title(),
        )


    with custody_2:

        st.metric(
            "Current Custodian",
            current_custodian,
        )


    st.subheader(
        "Responsibility Assessment"
    )


    responsibility_1, responsibility_2 = (
        st.columns(2)
    )


    with responsibility_1:

        st.metric(
            "Responsible Party",
            responsible_party,
        )


    with responsibility_2:

        st.metric(
            "Required Action",
            required_action,
        )


# ---------------------------------------------------------
# Journey completion
# ---------------------------------------------------------

st.divider()


st.subheader(
    "✅ Guided investigation complete"
)


st.write(
    (
        "You followed one shipment from an operational signal "
        "through investigation, responsibility and next action."
    )
)


st.markdown(
    """
    **This was one shipment.**

    LISA is designed to apply the same operational reasoning
    across larger shipment datasets so teams can focus on the
    cases that require attention instead of manually reviewing
    every tracking event.
    """
)


explore_column, command_column = (
    st.columns(2)
)


with explore_column:

    st.button(
        "🔄 Explore another shipment",
        on_click=clear_custody_selection,
        width="stretch",
    )


with command_column:

    if st.button(
        "📊 Return to Command Centre",
        type="primary",
        width="stretch",
    ):

        st.switch_page(
            "pages/operations.py"
        )


# ---------------------------------------------------------
# Public demo boundary
# ---------------------------------------------------------

with st.expander(
    "About this responsibility assessment"
):

    st.write(
        """
        This public demonstration uses simplified custody
        and responsibility classifications based on synthetic
        shipment states.

        The private LISA platform uses a more detailed,
        evidence-based operational intelligence model with
        broader routing, lifecycle, validation and responsibility
        logic.
        """
    )


render_feedback()