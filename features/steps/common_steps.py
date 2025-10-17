from behave import given
from utils.driver_factory import create_edge_driver

@given("I am on the Discover home page")
def step_open_home(context):
    if not hasattr(context, "base_url"):
        context.base_url = "https://tmdb-discover.surge.sh/"
        print("[WARN] base_url was missing; set default.")
    if not hasattr(context, "driver") or context.driver is None:
        print("[WARN] driver was missing; creating Edge (selenium-wire) inline.")
        context.driver = create_edge_driver(headless=False, use_selenium_wire=True)
    context.driver.get(context.base_url)
