Feature: Logout functionality

  Scenario: Logout
    Given I am logged in
    When I click the logout button
    Then I should be logged out and redirected to the login page
