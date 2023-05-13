from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

def test_navigate_to_cart(driver, login):
    inventory_page = InventoryPage(driver)
    inventory_page.go_to_cart_page()
    assert driver.current_url == 'https://www.saucedemo.com/cart.html'
