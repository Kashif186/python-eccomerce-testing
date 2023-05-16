from pages.inventory_page import InventoryPage

def test_add_to_cart_visual(driver, login, eyes):
    with eyes.open(driver, "Ecommerce App", "Add to Cart") as eyes_session:
        inventory_page = InventoryPage(driver)
        inventory_page.add_item_to_cart()
        eyes_session.check_window("Item added to cart")
