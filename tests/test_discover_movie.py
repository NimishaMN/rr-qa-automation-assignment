# tests/test_discover_movie.py
import time
from selenium.webdriver.common.by import By
from tests.utils_net import wait_for_call, API_KEY

def open_home(driver, base_url):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    driver.get(base_url)
    WebDriverWait(driver, 30).until(
        EC.any_of(
            EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Popular')]")),
            EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Newest')]")),
            EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Trending')]")),
        )
    )
    time.sleep(0.3)

def click_category(driver, *labels, timeout=10):
    # flexible clicker (same as before); short version for brevity:
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    end = time.time() + timeout
    while time.time() < end:
        for label in labels:
            xp = f"//button[contains(translate(., 'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), '{label.upper()}')]"
            els = driver.find_elements(By.XPATH, xp)
            if els:
                el = els[0]
                try:
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(el))
                except Exception:
                    pass
                try:
                    el.click()
                except Exception:
                    driver.execute_script("arguments[0].click();", el)
                time.sleep(0.5)
                return
        time.sleep(0.25)
    raise AssertionError(f"Could not click any of: {labels}")

def test_newest_calls_now_playing(driver, base_url):
    """
    Clicking 'Newest' triggers:
      GET /3/movie/now_playing?page=1&api_key=...
    """
    open_home(driver, base_url)
    click_category(driver, "Newest", "Now Playing")  # UI label may vary

    req = wait_for_call(
        driver,
        r"/3/movie/now_playing$",
        expected_params={"page": "1"},
        timeout=60,
    )
    assert req.response.status_code == 200

def test_popular_calls_movie_popular(driver, base_url):
    """
    Clicking 'Popular' triggers:
      GET /3/movie/popular?page=1&api_key=...
    """
    open_home(driver, base_url)
    click_category(driver, "Popular")

    req = wait_for_call(
        driver,
        r"/3/movie/popular$",
        expected_params={"page": "1"},
        timeout=60,
    )
    assert req.response.status_code == 200

def test_filtering_discovers_movie(driver, base_url):
    """
    Filtering triggers:
      /3/discover/movie?sort_by=popularity.desc
                         &release_date.gte=1903-01-01
                         &release_date.lte=2025-12-31
                         &vote_average.gte=0
                         &vote_average.lte=5
                         &page=1
                         &with_genres=28
                         &api_key=...
    """
    open_home(driver, base_url)

    # --- Interact with UI to set filters (tweak selectors if your page differs) ---
    # Example: click "Filters" if hidden, pick Genre=Action(28), Rating 0..5, Year range
    try:
        # Genre: assume a menu/searchable list — pick "Action"
        # If you have a select/dropdown, adjust to your actual DOM
        driver.find_element(By.XPATH, "//label[contains(., 'Genre')]/following::button[1]").click()
        time.sleep(0.2)
        driver.find_element(By.XPATH, "//li[contains(., 'Action')]").click()
    except Exception:
        pass

    # Rating max 5
    try:
        # if there are two inputs for rating min/max, set max to 5 and min to 0
        # update selectors to match your app's markup
        max_rating = driver.find_element(By.CSS_SELECTOR, "[data-testid='rating-max'] input")
        max_rating.clear(); max_rating.send_keys("5")
        min_rating = driver.find_element(By.CSS_SELECTOR, "[data-testid='rating-min'] input")
        min_rating.clear(); min_rating.send_keys("0")
    except Exception:
        pass

    # Dates (release_date.gte / lte)
    try:
        start = driver.find_element(By.CSS_SELECTOR, "[data-testid='date-start'] input")
        end   = driver.find_element(By.CSS_SELECTOR, "[data-testid='date-end'] input")
        start.clear(); start.send_keys("1903-01-01")
        end.clear();   end.send_keys("2025-12-31")
    except Exception:
        pass

    time.sleep(2)  # allow filter change to trigger the network call

    req = wait_for_call(
        driver,
        r"/3/discover/movie$",
        expected_params={
            "sort_by": "popularity.desc",
            "release_date.gte": "1903-01-01",
            "release_date.lte": "2025-12-31",
            "vote_average.gte": "0",
            "vote_average.lte": "5",
            "with_genres": "28",
            "page": "1",
        },
        timeout=60,
        subset=True,   # server may add extra params; we only assert the important ones + api_key
    )
    assert req.response.status_code == 200
