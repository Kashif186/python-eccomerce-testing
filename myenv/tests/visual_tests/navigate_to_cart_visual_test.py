from pages.inventory_page import InventoryPage

def test_navigate_to_cart_visual(driver, login, eyes):
    with eyes.open(driver, "Ecommerce App", "Navigate to Cart") as eyes_session:
        inventory_page = InventoryPage(driver)
        inventory_page.go_to_cart_page()

        eyes_session.check_window("Cart page displayed")
