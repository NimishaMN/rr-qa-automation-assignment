from utils.driver_factory import create_edge_driver

driver = create_edge_driver(headless=False)
driver.get("https://tmdb-discover.surge.sh/")
print(driver.title)
driver.quit()
