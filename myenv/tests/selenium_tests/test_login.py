from pages.inventory_page import InventoryPage

def test_login_success(driver, login):
    inventory_page = InventoryPage(driver)
    assert driver.current_url == 'https://www.saucedemo.com/inventory.html'
