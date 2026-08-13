def classify_demo_route(
    expected_hub: str,
    observed_hub: str,
) -> str:
    """
    Simplified public routing example.
    """

    if expected_hub == observed_hub:
        return "CORRECT_ROUTE"

    return "ROUTE_EXCEPTION"


if __name__ == "__main__":
    print(
        classify_demo_route(
            expected_hub="HUB_A",
            observed_hub="HUB_B",
        )
    )