*** Settings ***
Documentation    Remove item from cart
Resource          config.robot
Resource          common_setup_teardown.robot
Library           SeleniumLibrary
Suite Setup       Common Setup
Suite Teardown    Common Teardown

*** Test Cases ***
Remove Item from Cart
    [Tags]    RemoveFromCart
    Click Button    class=btn_primary    # Add item to cart
    Click Link    class=shopping_cart_link
    Click Button    class=btn_secondary    # Remove item from cart
    Element Should Not Be Visible    class=shopping_cart_badge
