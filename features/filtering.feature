Feature: Filtering options

  Background:
    Given I am on the Discover home page

  @smoke
  Scenario: Switching categories updates the grid
    When I switch to "Top Rated"
    Then I should see the list updated

  Scenario: Title search narrows results
    When I search for titles with "a"
    Then I should see at least 1 result

  Scenario: Type filter Movies vs TV
    When I select type "Movies"
    Then I should see results

  Scenario: Year >= 2000 and Rating >= 8
    When I set year to 2000 and rating to 8
    Then I should see results

  Scenario: Genre filter Drama
    When I choose genre "Drama"
    Then I should see results
