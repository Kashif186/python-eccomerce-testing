from behave import given, when, then
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage



@given('I have an item in the cart')
def add_item_to_cart(context):
    inventory_page = InventoryPage(context.driver)
    inventory_page.add_item_to_cart()
    assert inventory_page.get_cart_count().__eq__('1')

@when('I remove the item from the cart')
def remove_item_from_cart(context):
    inventory_page = InventoryPage(context.driver)
    inventory_page.go_to_cart_page()
    cart_page = CartPage(context.driver)
    cart_page.remove_item_from_cart()

@then('the cart count should be decreased by 1')
def verify_cart_count(context):
    cart_page = CartPage(context.driver)
    assert cart_page.get_cart_count().__eq__('0')
