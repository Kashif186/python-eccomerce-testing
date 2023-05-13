from pages.inventory_page import InventoryPage

def test_add_to_cart(driver, login):
    inventory_page = InventoryPage(driver)
    inventory_page.add_item_to_cart()
    assert inventory_page.get_cart_count().__eq__('1')