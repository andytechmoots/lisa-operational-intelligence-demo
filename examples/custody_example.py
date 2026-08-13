def classify_demo_custody(status: str) -> str:
    """
    Simplified public demonstration only.

    The production/private LISA intelligence layer
    uses a more detailed evidence-based ruleset.
    """

    if status == "DELIVERED":
        return "COMPLETED"

    if status == "RETURN_TO_SHIPPER":
        return "RETURN_FLOW"

    return "CONTRACTOR"


if __name__ == "__main__":
    examples = [
        "DELIVERED",
        "AT_CONTRACTOR_HUB",
        "RETURN_TO_SHIPPER",
    ]

    for status in examples:
        print(
            status,
            "=>",
            classify_demo_custody(status),
        )