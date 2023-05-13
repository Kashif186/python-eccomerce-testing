from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class CartPage:
    def __init__(self, driver):
        self.driver = driver

        # Locators
        self.remove_backpack_to_cart_buttons = (By.XPATH, '//*[@id="remove-sauce-labs-backpack"]')
        self.cart_count = (By.CLASS_NAME, 'shopping_cart_badge')
        

    def remove_item_from_cart(self):
        self.driver.find_element(*self.cart_count).click()
        self.driver.find_element(*self.remove_backpack_to_cart_buttons).click()
    

    def get_cart_count(self):
        try:
            return self.driver.find_element(*self.cart_count).text
        except NoSuchElementException:
            return '0'
