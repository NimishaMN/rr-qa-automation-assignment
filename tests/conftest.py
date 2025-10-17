import pytest
from utils.driver_factory import create_edge_driver

@pytest.fixture(scope="session")
def base_url():
    return "https://tmdb-discover.surge.sh/"

@pytest.fixture(scope="session")
def driver():
    # IMPORTANT: selenium-wire enabled so driver.requests exists
    d = create_edge_driver(headless=False, use_selenium_wire=True)
    yield d
    d.quit()

@pytest.fixture(autouse=True)
def clear_requests(driver):
    if hasattr(driver, "requests"):
        try:
            driver.requests.clear()
        except Exception:
            pass
