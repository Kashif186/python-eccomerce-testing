*** Settings ***
Documentation    Navigate to cart page
Resource          config.robot
Resource          common_setup_teardown.robot
Library           SeleniumLibrary
Suite Setup       Common Setup
Suite Teardown    Common Teardown

*** Test Cases ***
Navigate to Cart Page
    [Tags]    NavigateToCart
    Click Link    class=shopping_cart_link
    Location Should Be    ${BASE_URL}/cart.html
