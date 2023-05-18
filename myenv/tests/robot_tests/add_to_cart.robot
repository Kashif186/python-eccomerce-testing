*** Settings ***
Documentation    Add item to cart
Resource          config.robot
Resource          common_setup_teardown.robot
Suite Setup       Common Setup
Suite Teardown    Common Teardown

*** Test Cases ***
Add Item to Cart
    [Tags]    AddToCart
    Click Button    class=btn_primary    # Add item to cart
    Element Should Be Visible    class=shopping_cart_badge


