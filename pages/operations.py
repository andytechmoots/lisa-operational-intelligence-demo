import streamlit as st

from components.data import load_shipments
from components.ui import (
    render_feedback,
    render_header,
    render_workflow,
)


shipments = load_shipments()


# ---------------------------------------------------------
# Session / scenario state
# ---------------------------------------------------------

if "review_started" not in st.session_state:
    st.session_state[
        "review_started"
    ] = False


def reset_demo() -> None:

    st.session_state[
        "review_started"
    ] = False

    st.session_state[
        "selected_waybill"
    ] = None

    st.session_state[
        "_investigation_waybill"
    ] = None

    st.session_state[
        "_custody_waybill"
    ] = None


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

render_header(
    "LISA — Logistics Intelligence & Shipment Analytics",
    (
        "Turn fragmented logistics data into "
        "operational understanding and action."
    ),
)


# ---------------------------------------------------------
# Executive scenario
# ---------------------------------------------------------

st.markdown(
    "## Imagine this scenario"
)

st.write(
    """
    You are responsible for **thousands of shipments**.

    Your executive asks you:
    """
)


st.markdown(
    """
<div class="scenario-box">
<div class="scenario-label">
Executive request
</div>

<div class="scenario-question">
“What needs our attention today, why is it happening,
and who needs to act?”
</div>

<div class="scenario-support">
You have tracking events, delivery statuses, hubs,
returns, routing exceptions and operational handoffs.

The problem is not getting more data.
The problem is knowing where to start.
</div>
</div>
""",
    unsafe_allow_html=True,
)


st.markdown(
    "### Where do you start?"
)


# ---------------------------------------------------------
# Start / restart control
# ---------------------------------------------------------

if not st.session_state[
    "review_started"
]:

    if st.button(
        "▶ SHOW ME WHAT NEEDS ATTENTION",
        type="primary",
        width="stretch",
        key="start_review",
    ):

        st.session_state[
            "review_started"
        ] = True

        st.rerun()


    st.caption(
        (
            "Start the review to see how LISA moves from "
            "operational signal → investigation → "
            "responsibility → action."
        )
    )


    render_feedback()

    st.stop()


else:

    status_column, restart_column = (
        st.columns(
            [4, 1]
        )
    )


    with status_column:

        st.success(
            (
                "Operational review started — "
                "LISA is surfacing the signals "
                "that may require attention."
            ),
            icon="✅",
        )


    with restart_column:

        st.button(
            "↻ Restart scenario",
            on_click=reset_demo,
            width="stretch",
        )


# ---------------------------------------------------------
# Workflow
# ---------------------------------------------------------

render_workflow()


# ---------------------------------------------------------
# Scenario metrics
# ---------------------------------------------------------

total_shipments = len(
    shipments
)


delivered = int(
    (
        shipments["status"]
        == "DELIVERED"
    ).sum()
)


route_exceptions = int(
    (
        shipments["route_status"]
        == "ROUTE_EXCEPTION"
    ).sum()
)


return_flow = int(
    (
        shipments["custody_type"]
        == "RETURN_FLOW"
    ).sum()
)


# ---------------------------------------------------------
# Step 1
# ---------------------------------------------------------

st.subheader(
    "Step 1 — LISA scans the operational picture"
)


st.write(
    (
        "Instead of manually reviewing every shipment, "
        "LISA begins by summarizing the network and "
        "surfacing situations that may require intervention."
    )
)


metric_1, metric_2, metric_3, metric_4 = (
    st.columns(4)
)


with metric_1:

    st.metric(
        "Shipments Monitored",
        total_shipments,
    )


with metric_2:

    st.metric(
        "Delivered",
        delivered,
    )


with metric_3:

    st.metric(
        "Need Routing Attention",
        route_exceptions,
    )


with metric_4:

    st.metric(
        "In Return Flow",
        return_flow,
    )


# ---------------------------------------------------------
# Attention signal
# ---------------------------------------------------------

if route_exceptions > 0:

    st.markdown(
        f"""
<div class="attention-box">
<strong>
⚠️ LISA found {route_exceptions} shipments requiring routing attention.
</strong>
<br><br>
Their observed routing position differs from the expected position.
Instead of reviewing every shipment, operations can now focus on
the cases that may require intervention.
</div>
""",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# Exception queue
# ---------------------------------------------------------

st.subheader(
    "Which shipments should we review first?"
)


exceptions = (
    shipments.loc[
        shipments[
            "route_status"
        ]
        == "ROUTE_EXCEPTION",
        [
            "waybill",
            "destination",
            "expected_hub",
            "observed_hub",
            "status",
        ],
    ]
    .copy()
)


exceptions[
    "problem"
] = "Routing Exception"


exceptions[
    "action"
] = "Investigate"


exceptions = exceptions.rename(
    columns={
        "waybill":
            "Shipment",

        "destination":
            "Destination",

        "expected_hub":
            "Expected Hub",

        "observed_hub":
            "Observed Hub",

        "status":
            "Current Status",

        "problem":
            "Signal",

        "action":
            "Next Step",
    }
)


st.dataframe(
    exceptions,
    hide_index=True,
    width="stretch",
)


# ---------------------------------------------------------
# Guided example
# ---------------------------------------------------------

st.subheader(
    "Follow one case through LISA"
)


st.markdown(
    """
<div class="next-step-box">
<strong>
SYN0002 has been flagged for investigation.
</strong>
<br><br>
Expected routing location: <strong>HUB_B</strong><br>
Observed routing location: <strong>HUB_C</strong><br><br>

The next question is not simply
“Where is the shipment?”

It is:

<strong>
“What happened, who owns the issue,
and what should happen next?”
</strong>
</div>
""",
    unsafe_allow_html=True,
)


if st.button(
    "🔎 INVESTIGATE SYN0002 →",
    type="primary",
    width="stretch",
):

    st.session_state[
        "selected_waybill"
    ] = "SYN0002"

    st.session_state[
        "_investigation_waybill"
    ] = "SYN0002"

    st.switch_page(
        "pages/investigation.py"
    )


st.caption(
    (
        "SYN0002 is the guided example. "
        "Once inside Shipment Investigation, "
        "you can select other synthetic shipments "
        "and compare different outcomes."
    )
)


# ---------------------------------------------------------
# Product breadth
# ---------------------------------------------------------

st.divider()


st.subheader(
    "What this demo demonstrates"
)


capability_1, capability_2, capability_3, capability_4 = (
    st.columns(4)
)


with capability_1:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 👁 Network Visibility"
        )

        st.write(
            (
                "Understand delivery performance, "
                "SLA exposure and operational position."
            )
        )


with capability_2:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 📦 Shipment Intelligence"
        )

        st.write(
            (
                "Reconstruct shipment journeys "
                "and detect abnormal behaviour."
            )
        )


with capability_3:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 🔎 Investigation"
        )

        st.write(
            (
                "Move from network-level signals "
                "to shipment-level evidence."
            )
        )


with capability_4:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 🧭 Responsibility & Action"
        )

        st.write(
            (
                "Determine ownership and translate "
                "evidence into an operational next step."
            )
        )


# ---------------------------------------------------------
# Public/private boundary
# ---------------------------------------------------------

st.info(
    (
        "This public experience demonstrates selected LISA workflows "
        "using synthetic shipment data. The private LISA platform "
        "contains a broader operational-intelligence architecture, "
        "additional validation logic and more detailed decision rules."
    ),
    icon="ℹ️",
)


# ---------------------------------------------------------
# Supporting data
# ---------------------------------------------------------

with st.expander(
    "View supporting network-level demo data"
):

    st.subheader(
        "Operational Flow"
    )


    status_counts = (
        shipments[
            "status"
        ]
        .value_counts()
        .rename_axis(
            "Status"
        )
        .reset_index(
            name="Shipments"
        )
    )


    st.bar_chart(
        status_counts,
        x="Status",
        y="Shipments",
    )


    left_column, right_column = (
        st.columns(2)
    )


    with left_column:

        st.subheader(
            "Routing Position"
        )


        route_counts = (
            shipments[
                "route_status"
            ]
            .value_counts()
            .rename_axis(
                "Routing Status"
            )
            .reset_index(
                name="Shipments"
            )
        )


        st.dataframe(
            route_counts,
            hide_index=True,
            width="stretch",
        )


    with right_column:

        st.subheader(
            "Shipment Snapshot"
        )


        st.dataframe(
            shipments[
                [
                    "waybill",
                    "destination",
                    "status",
                    "route_status",
                ]
            ],
            hide_index=True,
            width="stretch",
        )


render_feedback()