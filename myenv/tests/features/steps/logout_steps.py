from behave import when, then
from pages.inventory_page import InventoryPage
from pages.menu_page import MenuPage

@when('I click the logout button')
def click_logout_button(context):
    inventory_page = InventoryPage(context.driver)
    inventory_page.open_menu()
    menu_page = MenuPage(context.driver)
    menu_page.logout()
    

@then('I should be logged out and redirected to the login page')
def verify_logout(context):
    assert context.driver.current_url == 'https://www.saucedemo.com/'
