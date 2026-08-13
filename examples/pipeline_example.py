def run_demo_pipeline() -> None:
    """
    Public conceptual pipeline example.

    Proprietary operational intelligence rules
    are intentionally excluded.
    """

    stages = [
        "Generate synthetic data",
        "Validate schema",
        "Transform shipment events",
        "Build warehouse records",
        "Calculate demo KPIs",
        "Run validation checks",
    ]

    for index, stage in enumerate(
        stages,
        start=1,
    ):
        print(
            f"[{index}/{len(stages)}] {stage}"
        )


if __name__ == "__main__":
    run_demo_pipeline()