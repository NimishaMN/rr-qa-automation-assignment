from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


def _wait_for_pager(driver, timeout=10):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//a[@role='button' and starts-with(@aria-label,'Page ')]"))
    )


def _click_page(driver, n: int, timeout=10):
    _wait_for_pager(driver, timeout)
    xp_num = f"//a[@role='button' and normalize-space()='{n}']"
    xp_aria = f"//a[@role='button' and @aria-label='Page {n}']"

    link = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, f"({xp_num} | {xp_aria})[1]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", link)
    try:
        link.click()
    except Exception:
        driver.execute_script("arguments[0].click();", link)

    time.sleep(0.5)


def _active_page_text(driver):
    active_as = driver.find_elements(By.XPATH, "//a[@role='button' and @aria-current='page']")
    if active_as:
        return active_as[0].text.strip()

    selected = driver.find_elements(By.XPATH, "//li[contains(@class,'selected')]//a[@role='button']")
    if selected:
        return selected[0].text.strip()

    return ""


@when("I move to page 2")
def step_page2(context):
    try:
        _click_page(context.driver, 2)
    except TimeoutException:
        raise AssertionError("Pagination link for page 2 not found")


@when("I move to page 1")
def step_page1(context):
    try:
        _click_page(context.driver, 1)
    except TimeoutException:
        raise AssertionError("Pagination link for page 1 not found")


@then('the active page should be "{n}"')
def step_active_page(context, n):
    _wait_for_pager(context.driver, 10)
    active = _active_page_text(context.driver)
    assert active == n, f'Expected active page "{n}", but got "{active or "[none]"}"'
