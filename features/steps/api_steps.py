# features/steps/api_steps.py
from behave import when, then
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.api_assert import wait_for_call



def _tab_xpath_ci(label: str) -> str:
    L, U = "abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return f"//a[contains(translate(normalize-space(.),'{L}','{U}'),'{label.upper()}')]"

def _click_tab(driver, *labels, timeout=10):
    end = time.time() + timeout
    while time.time() < end:
        for label in labels:
            xp = _tab_xpath_ci(label)
            els = [e for e in driver.find_elements(By.XPATH, xp) if e.is_displayed()]
            if not els:
                continue
            el = els[0]
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xp)))
            except Exception:
                pass
            try:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                el.click()
            except Exception:
                driver.execute_script("arguments[0].click();", el)
            time.sleep(0.4)
            return
        time.sleep(0.2)
    raise AssertionError(f"Could not click any of: {labels}")

def _find_search_input(driver, timeout=10):
    L, U = "abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    xps = [
        "//input[@name='search']",
        f"//input[translate(@placeholder,'{L}','{U}')='SEARCH']",
    ]
    end = time.time() + timeout
    while time.time() < end:
        for xp in xps:
            els = [e for e in driver.find_elements(By.XPATH, xp) if e.is_displayed()]
            if els:
                return els[0]
        time.sleep(0.2)
    raise AssertionError("Search input not found")

def _click_combobox_option(driver, label_text, option_text):
    box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//p[normalize-space()='{label_text}']/following::*[@role='combobox'][1]")
        )
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", box)
    box.click()

    try:
        input_el = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[starts-with(@id,'react-select') and self::input]")
            )
        )
        input_el.send_keys(option_text, Keys.ENTER)
        return
    except Exception:
        pass

    opt = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//*[@role='option' and normalize-space()='{option_text}']")
        )
    )
    opt.click()

@when('I click the "{label}" tab')
def step_click_tab(context, label):
    if label.strip().upper() == "TREND":
        _click_tab(context.driver, "Trend", "Trending")
    else:
        _click_tab(context.driver, label)

@when('I click the "SEARCH" tab and search for "{text}"')
def step_search_movies(context, text):
    box = _find_search_input(context.driver)
    box.clear()
    box.click()
    box.send_keys(text)
    box.send_keys(Keys.ENTER)
    time.sleep(0.6)

@when('I set Type to "TV" and Genre to "Comedy"')
def step_set_type_tv_genre_comedy(context):
    d = context.driver

    # --- Set Type: "TV" ---
    type_input = WebDriverWait(d, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[starts-with(@id,'react-select-2-input')]"))
    )
    d.execute_script("arguments[0].scrollIntoView({block:'center'});", type_input)
    type_input.send_keys("TV Shows")
    type_input.send_keys(Keys.ENTER)
    time.sleep(1)

    # --- Set Genre: "Comedy" ---
    genre_input = WebDriverWait(d, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[starts-with(@id,'react-select-3-input')]"))
    )
    d.execute_script("arguments[0].scrollIntoView({block:'center'});", genre_input)
    genre_input.send_keys("Comedy")
    genre_input.send_keys(Keys.ENTER)
    time.sleep(1)


@then('an API call is made to "movie popular" page {page:d}')
def step_movie_popular(context, page):
    res = wait_for_call(context.driver, r"/3/movie/popular$", expected_params={"page": str(page)}, timeout=30)
    assert res.response.status_code == 200

@then('an API call is made to "trending movie week" page {page:d}')
def step_trending_movie_week(context, page):
    res = wait_for_call(context.driver, r"/3/trending/movie/week$", expected_params={"page": str(page)}, timeout=30)
    assert res.response.status_code == 200

@then('an API call is made to "movie now playing" page {page:d}')
def step_now_playing(context, page):
    res = wait_for_call(context.driver, r"/3/movie/now_playing$", expected_params={"page": str(page)}, timeout=30)
    assert res.response.status_code == 200

@then('an API call is made to "movie top rated" page {page:d}')
def step_movie_top_rated(context, page):
    res = wait_for_call(context.driver, r"/3/movie/top_rated$", expected_params={"page": str(page)}, timeout=30)
    assert res.response.status_code == 200

@then('a "search movie" API call occurs with query "{text}" page {page:d}')
def step_search_movie(context, text, page):
    res = wait_for_call(
        context.driver,
        r"/3/search/movie$",
        expected_params={"query": text, "page": str(page)},
        timeout=30,
    )
    assert res.response.status_code == 200

@then('a "discover movie" API call occurs with params')
def step_discover_movie_with_params(context):
    # Only assert what the scenario table provides (e.g., with_genres + page)
    expected = {row['key']: row['value'] for row in context.table}
    res = wait_for_call(context.driver, r"/3/discover/movie$", expected_params=expected, timeout=45)
    assert res.response.status_code == 200

@then('a "discover tv" API call occurs with params')
def step_discover_tv_with_params(context):
    expected = {row['key']: row['value'] for row in context.table}
    res = wait_for_call(context.driver, r"/3/discover/tv$", expected_params=expected, timeout=45)
    assert res.response.status_code == 200
