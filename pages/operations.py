import streamlit as st

from components.data import load_shipments
from components.ui import (
    render_feedback,
    render_header,
)


shipments = load_shipments()


render_header(
    "LISA — Operations Command Centre",
    (
        "Last-mile operational intelligence "
        "from synthetic shipment data."
    ),
)


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


column_1, column_2, column_3, column_4 = (
    st.columns(4)
)

with column_1:
    st.metric(
        "Total Shipments",
        total_shipments,
    )

with column_2:
    st.metric(
        "Delivered",
        delivered,
    )

with column_3:
    st.metric(
        "Route Exceptions",
        route_exceptions,
    )

with column_4:
    st.metric(
        "Return Flow",
        return_flow,
    )


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
        use_container_width=True,
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
        use_container_width=True,
    )
render_feedback()