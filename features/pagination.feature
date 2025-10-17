Feature: Pagination

  Background:
    Given I am on the Discover home page

  Scenario: Go to page 2 and back
    When I move to page 2
    Then the active page should be "2"
    When I move to page 1
    Then the active page should be "1"
