from behave import *
from pages.login_page import LoginPage

@given('the user is on the login page')
def step_user_on_login_page(context):
    context.driver.get('https://www.saucedemo.com/')
    assert context.driver.current_url == 'https://www.saucedemo.com/'

@when('they enter valid credentials')
def step_enter_valid_credentials(context):
    login_page = LoginPage(context.driver)
    login_page.enter_username('standard_user')
    login_page.enter_password('secret_sauce')


@when('they click the login button')
def step_click_login_button(context):
    login_page = LoginPage(context.driver)
    login_page.click_login_button()


@then('they should be redirected to the inventory page')
def step_redirected_to_inventory_page(context):
    assert context.driver.current_url == 'https://www.saucedemo.com/inventory.html'