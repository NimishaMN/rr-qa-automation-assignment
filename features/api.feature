Feature: Network assertions
  Validates that network API calls match expected endpoints and parameters.

  Background:
    Given I am on the Discover home page

  Scenario: Discover request includes filters
    When I set rating to 8
    Then I should observe a discover or search network call with rating "8"

  Scenario: Popular movies page 2 loads via API
    When I click the "Popular" tab for Movies and go to page 2
    Then an API call is made to "movie popular" page 2

  Scenario: Trending TV this week
    When I select "Trending" and "TV Shows" with window "week"
    Then an API call is made to "trending tv week" page 1

  Scenario: Discover newest movies (sorted by release desc)
    When I select "Newest" and page 1
    Then an API call is made to "discover newest movies" page 1

  Scenario: Discover movies with filters
    When I set Genre to "Drama", Rating to "8", Year to "2000"
    Then a "discover movie" API call occurs with params
      | key                  | value |
      | with_genres          | 18    |
      | vote_average.gte     | 8     |
      | primary_release_year | 2000  |
      | page                 | 1     |

  Scenario: Search TV titles for "office"
    When I type "office" in the title search
    Then a "search tv" API call occurs with query "office" page 1
