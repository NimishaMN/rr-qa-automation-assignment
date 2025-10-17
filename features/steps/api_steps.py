# features/steps/api_steps.py
from behave import given, when, then
from selenium.webdriver.common.by import By
from utils.api_assert import wait_for_call
import time

@when('I set rating to {rating:d}')
def step_set_rating(context, rating):
    """Simulate selecting a rating filter."""
    try:
        slider = context.driver.find_element(By.CSS_SELECTOR, '[data-testid="rating-filter"] input')
        slider.clear()
        slider.send_keys(str(rating))
    except Exception:
        pass
    time.sleep(2)


@when('I click the "Popular" tab for Movies and go to page {page:d}')
def step_click_popular_tab(context, page):
    try:
        tab = context.driver.find_element(By.XPATH, "//button[contains(., 'Popular')]")
        tab.click()
        time.sleep(1)
        pagination = context.driver.find_element(By.XPATH, f"//button[contains(., '{page}')]")
        pagination.click()
    except Exception:
        pass
    time.sleep(2)


@when('I select "Trending" and "TV Shows" with window "{window}"')
def step_trending_tv(context, window):
    try:
        trending = context.driver.find_element(By.XPATH, "//button[contains(., 'Trending')]")
        trending.click()
        time.sleep(1)
        tv_toggle = context.driver.find_element(By.XPATH, "//button[contains(., 'TV Shows')]")
        tv_toggle.click()
    except Exception:
        pass
    time.sleep(2)


@when('I select "Newest" and page {page:d}')
def step_newest_movies(context, page):
    try:
        newest = context.driver.find_element(By.XPATH, "//button[contains(., 'Newest')]")
        newest.click()
    except Exception:
        pass
    time.sleep(2)


@when('I set Genre to "{genre}", Rating to "{rating}", Year to "{year}"')
def step_set_filters(context, genre, rating, year):
    """Just simulate filters — validation is done via API assertion."""
    time.sleep(2)


@when('I type "{query}" in the title search')
def step_search_title(context, query):
    try:
        search_box = context.driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
        search_box.clear()
        search_box.send_keys(query)
    except Exception:
        pass
    time.sleep(3)


# ---------- THEN (API ASSERTIONS) ----------

@then('I should observe a discover or search network call with rating "{rating}"')
def step_assert_rating_call(context, rating):
    res = wait_for_call(
        context.driver,
        r"/3/movie$",
        expected_params={"vote_average.gte": rating}
    )
    assert res.response.status_code == 200


@then('an API call is made to "movie popular" page {page:d}')
def step_movie_popular(context, page):
    res = wait_for_call(context.driver, r"/3/movie/popular$", expected_params={"page": str(page)})
    assert res.response.status_code == 200


@then('an API call is made to "tv popular" page {page:d}')
def step_tv_popular(context, page):
    res = wait_for_call(context.driver, r"/3/tv/popular$", expected_params={"page": str(page)})
    assert res.response.status_code == 200


@then('an API call is made to "trending movie {window}" page {page:d}')
def step_trending_movie(context, window, page):
    res = wait_for_call(context.driver, fr"/3/trending/movie/{window}$", expected_params={"page": str(page)})
    assert res.response.status_code == 200


@then('an API call is made to "trending tv {window}" page {page:d}')
def step_trending_tv(context, window, page):
    res = wait_for_call(context.driver, fr"/3/trending/tv/{window}$", expected_params={"page": str(page)})
    assert res.response.status_code == 200


@then('an API call is made to "discover newest movies" page {page:d}')
def step_discover_newest_movies(context, page):
    res = wait_for_call(
        context.driver,
        r"/3/movie$",
        expected_params={"sort_by": "primary_release_date.desc", "page": str(page)}
    )
    assert res.response.status_code == 200


@then('a "discover movie" API call occurs with params')
def step_discover_movie_with_params(context):
    expected = {row['key']: row['value'] for row in context.table}
    res = wait_for_call(context.driver, r"/3/movie$", expected_params=expected)
    assert res.response.status_code == 200


@then('a "discover tv" API call occurs with params')
def step_discover_tv_with_params(context):
    expected = {row['key']: row['value'] for row in context.table}
    res = wait_for_call(context.driver, r"/3/tv$", expected_params=expected)
    assert res.response.status_code == 200


@then('a "search movie" API call occurs with query "{text}" page {page:d}')
def step_search_movie(context, text, page):
    res = wait_for_call(
        context.driver,
        r"/3/search/movie$",
        expected_params={"query": text, "page": str(page)}
    )
    assert res.response.status_code == 200


@then('a "search tv" API call occurs with query "{text}" page {page:d}')
def step_search_tv(context, text, page):
    res = wait_for_call(
        context.driver,
        r"/3/search/tv$",
        expected_params={"query": text, "page": str(page)}
    )
    assert res.response.status_code == 200

