from behave import given, when, then
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

@given('I am logged in')
def login(context):
    login_page = LoginPage(context.driver)
    login_page.enter_username('standard_user')
    login_page.enter_password('secret_sauce')
    login_page.click_login_button()
    assert context.driver.current_url == 'https://www.saucedemo.com/inventory.html'

@when('I add an item to the cart')
def add_item_to_cart(context):
    inventory_page = InventoryPage(context.driver)
    inventory_page.add_item_to_cart()

@then('the cart count should be increased by 1')
def verify_cart_count(context):
    inventory_page = InventoryPage(context.driver)
    cart_count = inventory_page.get_cart_count()
    assert cart_count.__eq__('1')
