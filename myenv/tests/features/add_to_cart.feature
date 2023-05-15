Feature: Add item to cart

  Scenario: Add item to cart
    Given I am logged in
    When I add an item to the cart
    Then the cart count should be increased by 1
