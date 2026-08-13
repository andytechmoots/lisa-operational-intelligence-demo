from examples.custody_example import classify_demo_custody
from examples.routing_example import classify_demo_route


def test_demo_custody_delivered():
    assert classify_demo_custody(
        "DELIVERED"
    ) == "COMPLETED"


def test_demo_custody_return_flow():
    assert classify_demo_custody(
        "RETURN_TO_SHIPPER"
    ) == "RETURN_FLOW"


def test_demo_custody_contractor():
    assert classify_demo_custody(
        "AT_CONTRACTOR_HUB"
    ) == "CONTRACTOR"


def test_demo_route_correct():
    assert classify_demo_route(
        "HUB_A",
        "HUB_A",
    ) == "CORRECT_ROUTE"


def test_demo_route_exception():
    assert classify_demo_route(
        "HUB_A",
        "HUB_B",
    ) == "ROUTE_EXCEPTION"