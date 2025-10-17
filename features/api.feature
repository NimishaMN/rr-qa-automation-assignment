Feature: Network assertions
  Validates that network API calls match expected endpoints and parameters.

  Background:
    Given I am on the Discover home page

  Scenario: Popular movies page 1 loads via API
    When I click the "Popular" tab
    Then an API call is made to "movie popular" page 1

  Scenario: Trending (movie, week) loads via API
    When I click the "Trend" tab
    Then an API call is made to "trending movie week" page 1

  Scenario: Newest loads now playing (movies)
    When I click the "Newest" tab
    Then an API call is made to "movie now playing" page 1

  Scenario: Top rated movies page 1 loads via API
    When I click the "Top rated" tab
    Then an API call is made to "movie top rated" page 1

  Scenario: Search movies for "war"
    When I click the "SEARCH" tab and search for "war"
    Then a "search movie" API call occurs with query "war" page 1

  Scenario: Discover options for TV, Genre=Comedy
  When I set Type to "TV" and Genre to "Comedy"
  Then a "discover tv" API call occurs with params
    | key         | value |
    | with_genres | 35    |
    | page        | 1     |

