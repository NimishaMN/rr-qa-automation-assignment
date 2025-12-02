from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from tests.utils_net import wait_for_call, API_KEY
from selenium.webdriver.common.keys import Keys

def _tab_xpath_ci(label: str) -> str:
    L = "abcdefghijklmnopqrstuvwxyz"
    U = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return (
        f"//*[self::a or self::button]"
        f"[contains(translate(normalize-space(.), '{L}','{U}'), '{label.upper()}')]"
    )


def open_home(driver, base_url):
    driver.get(base_url)
    WebDriverWait(driver, 30).until(
        EC.any_of(
            EC.presence_of_element_located((By.XPATH, _tab_xpath_ci("Popular"))),
            EC.presence_of_element_located((By.XPATH, _tab_xpath_ci("Newest"))),
            EC.presence_of_element_located((By.XPATH, _tab_xpath_ci("Trend"))),
            EC.presence_of_element_located((By.XPATH, _tab_xpath_ci("Top rated"))),
            EC.presence_of_element_located((By.XPATH, "//input[@name='search']")),
            # adding change for rebase trial
        )
    )
    time.sleep(0.3)


def click_category(driver, *labels, timeout=10):
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
            except TimeoutException:
                pass
            try:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                el.click()
            except ElementClickInterceptedException:
                driver.execute_script("arguments[0].click();", el)
            time.sleep(0.5)
            return
        time.sleep(0.25)
    raise AssertionError(f"Could not click any of: {labels}")

def _find_search_input(driver, timeout=10):
    L, U = "abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    xps = [
        "//input[@name='search']",
        f"//input[@type='text' and translate(@placeholder,'{L}','{U}')='SEARCH']",
    ]
    end = time.time() + timeout
    while time.time() < end:
        for xp in xps:
            els = [e for e in driver.find_elements(By.XPATH, xp) if e.is_displayed()]
            if els:
                return els[0]
        time.sleep(0.2)
    raise AssertionError("Search input not found")

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def go_to_page(driver, n, timeout=10):
    n = str(n)
    xp = (
        f"//a[@aria-label='Page {n}']"
        f"|//a[normalize-space(.)='{n}' and (@role='button' or @tabindex)]"
    )
    link = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xp))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", link)
    try:
        link.click()
    except Exception:
        driver.execute_script("arguments[0].click();", link)

    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//li[contains(@class,'selected')]//a[normalize-space(.)='{n}']|"
                           f"//li[contains(@class,'selected')][normalize-space(.)='{n}']")
            )
        )
    except Exception:
        time.sleep(0.4)  # fallback settle


def test_newest_calls_now_playing(driver, base_url):
    open_home(driver, base_url)
    click_category(driver, "Newest")

    req = wait_for_call(
        driver,
        r"/3/movie/now_playing$",
        expected_params={"page": "1"},
        timeout=30,
    )
    assert req.response.status_code == 200


def test_popular_calls_movie_page_2(driver, base_url):
    open_home(driver, base_url)
    click_category(driver, "Popular")
    go_to_page(driver, 2)

    req = wait_for_call(
        driver,
        r"/3/movie/popular$",
        expected_params={"page": "2"},
        subset=True,
        timeout=30,
    )
    assert req.response.status_code == 200

def test_search_titles(driver, base_url):
    open_home(driver, base_url)

    search_box = _find_search_input(driver)
    search_box.clear()
    search_box.click()
    search_box.send_keys("war")
    search_box.send_keys(Keys.ENTER)

    req = wait_for_call(
        driver,
        r"/3/search/(movie|tv)$",
        expected_params={"query": "war", "page": "1"},
        timeout=30,
        subset=True,
    )
    assert req.response.status_code == 200
