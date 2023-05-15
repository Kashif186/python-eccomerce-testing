from behave import when, then
from pages.inventory_page import InventoryPage


@when('I navigate to the cart page')
def navigate_to_cart_page(context):
    inventory_page = InventoryPage(context.driver)
    inventory_page.go_to_cart_page()

@then('the cart page should be displayed')
def verify_cart_page(context):
    assert context.driver.current_url == 'https://www.saucedemo.com/cart.html'
