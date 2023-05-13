from selenium.webdriver.common.by import By

class ConfirmationPage:
    def __init__(self, driver):
        self.driver = driver

        # Locators
        self.complete_header = (By.CLASS_NAME, 'complete-header')

    def get_complete_header_text(self):
        return self.driver.find_element(*self.complete_header).text
