from pages.inventory_page import InventoryPage
from pages.menu_page import MenuPage

def test_logout_visual(driver, login, eyes):
    with eyes.open(driver, "Ecommerce App", "Logout") as eyes_session:
        inventory_page = InventoryPage(driver)
        inventory_page.open_menu()
        menu_page = MenuPage(driver)
        menu_page.logout()

        eyes_session.check_window("Logged out")
