from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "synthetic"
    / "public_sample_shipments.csv"
)


@st.cache_data
def load_shipments() -> pd.DataFrame:
    dataframe = pd.read_csv(
        DATA_FILE,
        dtype={
            "waybill": str,
            "destination": str,
            "expected_hub": str,
            "observed_hub": str,
            "status": str,
        },
    )

    dataframe["route_status"] = (
        dataframe.apply(
            lambda row: (
                "CORRECT_ROUTE"
                if row["expected_hub"]
                == row["observed_hub"]
                else "ROUTE_EXCEPTION"
            ),
            axis=1,
        )
    )

    dataframe["custody_type"] = (
        dataframe["status"].map(
            {
                "DELIVERED": "COMPLETED",
                "RETURN_TO_SHIPPER": "RETURN_FLOW",
            }
        )
    )

    dataframe["custody_type"] = (
        dataframe["custody_type"].fillna(
            "CONTRACTOR"
        )
    )

    return dataframe