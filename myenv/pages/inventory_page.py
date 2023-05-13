from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class InventoryPage:
    def __init__(self, driver):
        self.driver = driver

        # Locators
        self.add_backpack_to_cart_buttons = (By.XPATH, '//*[@id="add-to-cart-sauce-labs-backpack"]')
        self.cart_count = (By.CLASS_NAME, 'shopping_cart_badge')
        self.cart_badge = (By.CLASS_NAME, 'shopping_cart_link')
        self.menu_button = (By.XPATH, '//button[@id="react-burger-menu-btn"]')


    def add_item_to_cart(self):
        self.driver.find_element(*self.add_backpack_to_cart_buttons).click()


    def get_cart_count(self):
        try:
            return self.driver.find_element(*self.cart_count).text
        except NoSuchElementException:
            return '0'
        
    
    def go_to_cart_page(self):
        self.driver.find_element(*self.cart_badge).click()

    
    def open_menu(self):
        self.driver.find_element(*self.menu_button).click()


    

