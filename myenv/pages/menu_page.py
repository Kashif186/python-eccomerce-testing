from selenium.webdriver.common.by import By
import time

class MenuPage:
    def __init__(self, driver):
        self.driver = driver

        # Locators
        self.logout_link = (By.ID, 'logout_sidebar_link')


    def logout(self):
        time.sleep(1)
        self.driver.find_element(*self.logout_link).click()
