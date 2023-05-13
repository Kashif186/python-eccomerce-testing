from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

def test_remove_from_cart(driver, login):
    inventory_page = InventoryPage(driver)
    inventory_page.add_item_to_cart()
    inventory_page.go_to_cart_page()
    cart_page = CartPage(driver)
    cart_page.remove_item_from_cart()
    assert cart_page.get_cart_count().__eq__('0')
