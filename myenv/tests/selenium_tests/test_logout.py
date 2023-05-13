from pages.inventory_page import InventoryPage
from pages.menu_page import MenuPage

def test_logout(driver, login):
    inventory_page = InventoryPage(driver)
    inventory_page.open_menu()
    menu_page = MenuPage(driver)
    menu_page.logout()
    assert driver.current_url == 'https://www.saucedemo.com/'
