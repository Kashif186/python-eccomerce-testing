Feature: Navigate to cart page

  Scenario: Navigate to cart page
    Given I am logged in
    When I navigate to the cart page
    Then the cart page should be displayed
