Feature: Remove item from cart

  Scenario: Remove item from cart
    Given I am logged in
    And I have an item in the cart
    When I remove the item from the cart
    Then the cart count should be decreased by 1
