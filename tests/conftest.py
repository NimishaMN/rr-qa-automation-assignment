import os
import pytest
from utils.driver_factory import create_edge_driver

@pytest.fixture(scope="session")
def base_url():
    return "https://tmdb-discover.surge.sh/"

@pytest.fixture(scope="session")
def driver():
    headless = os.getenv("HEADLESS", "0") in ("1", "true", "True")
    d = create_edge_driver(headless=headless, use_selenium_wire=True)
    try:
        d.set_page_load_timeout(60)
    except Exception:
        pass
    yield d
    d.quit()

@pytest.fixture(autouse=True)
def clear_requests(driver):
    if hasattr(driver, "requests"):
        try:
            driver.requests.clear()
        except Exception:
            pass
    yield
    if hasattr(driver, "requests"):
        try:
            driver.requests.clear()
        except Exception:
            pass
