from behave import when, then
from selenium.webdriver.common.by import By

@when("I move to page 2")
def step_page2(context):
    context.home.click((By.XPATH, "//button[normalize-space()='2']"))

@when("I move to page 1")
def step_page1(context):
    context.home.click((By.XPATH, "//button[normalize-space()='1']"))

@then('the active page should be "{n}"')
def step_active_page(context, n):
    # Simplest check: active button has aria-current or a selected class; adjust as needed
    btn = context.driver.find_element(By.XPATH, f"//button[normalize-space()='{n}']")
    # Try aria-current first
    aria = btn.get_attribute("aria-current")
    assert aria == "page" or "active" in (btn.get_attribute("class") or ""), "Page not active"
