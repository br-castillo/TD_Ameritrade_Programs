from splinter import Browser
from selenium import webdriver

# define path to chrome driver
executable_path = {'executable_path':r'#EXCUTABLE PATH TO SELENIUM WEBDRIVER HERE'}

# Set some default behaviors for browser
options = webdriver.ChromeOptions()

# make sure window is maximized
options.add_argument("--start-maximized")

# make sure notifications are off
options.add_argument("--disable-notifications")

# create a new browser object by default it is firefox
browser = Browser('chrome', 
	              **executable_path, 
	              headless = False, 
	              options = options)

browser.visit("https://www.instagram.com/accounts/login/?source=auth_switcher")

# find the username element
username_box = browser.find_by_name("username")
# login
username_box.fill("IG USERNAME")

# find the password
password = browser.find_by_name("password").fill("IG PASSWORD")

# submit button
submit = browser.find_by_class_name("sqdOP  L3NKy   y3zKF     ").first.click()
