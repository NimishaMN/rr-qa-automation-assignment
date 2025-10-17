from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
import os, subprocess

def create_edge_driver(headless=False, use_selenium_wire=False):
    driver_path = os.path.join(os.getcwd(), "drivers", "msedgedriver.exe")
    if not os.path.exists(driver_path):
        raise FileNotFoundError(f"EdgeDriver not found at {driver_path}")

    opts = EdgeOptions()
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--log-level=3")
    opts.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    if headless:
        opts.add_argument("--headless=new")

    service = EdgeService(driver_path, log_output=subprocess.DEVNULL)

    if use_selenium_wire:
        # create driver with selenium-wire so .requests is available
        from seleniumwire import webdriver as wire_webdriver
        seleniumwire_options = {
            # configure if you need a corporate proxy:
            # 'proxy': {'http': 'http://user:pass@host:port', 'https': 'https://user:pass@host:port'},
            'mitm_http2': True,
        }
        driver = wire_webdriver.Edge(service=service, options=opts,
                                     seleniumwire_options=seleniumwire_options)
    else:
        from selenium import webdriver
        driver = webdriver.Edge(service=service, options=opts)

    driver.set_page_load_timeout(30)
    return driver
