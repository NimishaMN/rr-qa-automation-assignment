from utils.driver_factory import create_edge_driver

def before_all(context):
    context.base_url = "https://tmdb-discover.surge.sh/"
    # IMPORTANT: enable selenium-wire
    context.driver = create_edge_driver(headless=False, use_selenium_wire=True)

def before_scenario(context, scenario):
    # start each scenario with a clean capture buffer
    if hasattr(context, "driver") and hasattr(context.driver, "requests"):
        try:
            context.driver.requests.clear()
        except Exception:
            pass

def after_all(context):
    if hasattr(context, "driver") and context.driver:
        context.driver.quit()
