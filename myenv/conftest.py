import pytest
from selenium import webdriver
from pages.login_page import LoginPage


@pytest.fixture(scope="function")
def driver():
    # Set up the ChromeDriver
    driver = webdriver.Chrome('drivers/chromedriver')
    yield driver
    # Teardown: Close the browser
    driver.quit()


@pytest.fixture
def login(driver):
    # Create a LoginPage instance
    login_page = LoginPage(driver)

    # Navigate to the login page
    driver.get('https://www.saucedemo.com/')

    # Perform the login
    login_page.enter_username('standard_user')
    login_page.enter_password('secret_sauce')
    login_page.click_login_button()


# Pytest configuration
def pytest_configure(config):
    # Add custom markers for BDD testing
    config.addinivalue_line(
        "markers", "feature: mark a test as a feature"
    )
    config.addinivalue_line(
        "markers", "scenario: mark a test as a scenario"
    )
