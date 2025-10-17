import os, subprocess
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions

def create_edge_driver(headless=False, use_selenium_wire=False):
    driver_path = os.path.join(os.getcwd(), "drivers", "msedgedriver.exe")
    if not os.path.exists(driver_path):
        raise FileNotFoundError(f"EdgeDriver not found at {driver_path}")

    opts = EdgeOptions()
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    opts.add_experimental_option("useAutomationExtension", False)
    if headless:
        opts.add_argument("--headless=new")

    service = EdgeService(driver_path, log_output=subprocess.DEVNULL)

    if use_selenium_wire:
        from seleniumwire import webdriver as wire_webdriver
        sw_opts = {
            "exclude_hosts": [],
            "proxy": {"verify_ssl": False},
        }
        driver = wire_webdriver.Edge(service=service, options=opts, seleniumwire_options=sw_opts)
    else:
        from selenium import webdriver
        driver = webdriver.Edge(service=service, options=opts)

    return driver
