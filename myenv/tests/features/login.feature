Feature: Login

  Scenario: Successful login
    Given the user is on the login page
    When they enter valid credentials
    And they click the login button
    Then they should be redirected to the inventory page
