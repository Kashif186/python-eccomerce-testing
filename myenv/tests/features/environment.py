from selenium import webdriver

def before_all(context):
	print("(**** TEST STARTED ****)")
	

def before_scenario(context, scenario):
	context.driver = webdriver.Chrome('drivers/chromedriver')  # Initialize the browser driver
	context.driver.get('https://www.saucedemo.com/')

def after_scenario(context, scenario):
	context.driver.quit()  # Close the browser

def after_all(context):
	print("(**** TEST COMPLETED ****)")
	