from behave import given, when, then
from pages.home_page import HomePage
from utils.logger import log
from seleniumwire.utils import decode

@when('I switch to "Top Rated"')
def step_switch_top_rated(context):
    context.first_title_before = (context.home.titles() or [""])[0]
    context.home.switch_to_top_rated()

@then("I should see the list updated")
def step_list_updated(context):
    titles = context.home.titles()
    assert titles, "No titles visible"
    assert titles[0] != context.first_title_before, "Grid did not update"

@when('I search for titles with "{q}"')
def step_search(context, q):
    context.home.search_title(q)

@then("I should see at least 1 result")
def step_has_results(context):
    assert len(context.home.titles()) > 0

@when('I select type "Movies"')
def step_type_movies(context):
    context.home.choose_movies()

@then("I should see results")
def step_any_results(context):
    assert len(context.home.titles()) > 0

@when("I set year to {year:d} and rating to {rating:d}")
def step_set_year_rating(context, year, rating):
    context.home.set_year(year)
    context.home.set_rating(rating)

@when('I choose genre "{genre}"')
def step_genre(context, genre):
    context.home.choose_genre(genre)
