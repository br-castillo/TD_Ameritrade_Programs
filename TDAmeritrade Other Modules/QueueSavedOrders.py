import time
import urllib
import requests
from splinter import Browser
from selenium import webdriver
from config import client_id, username, password, account_number, access_token, account_ID

# define headers
header = {'Authorization': "Bearer {}".format(access_token)}

# define the endpoint for saved orders, including your account_ID
endpoint = r"https://api.tdameritrade.com/v1/accounts/{}/savedorders".format(account_ID)

# make a post, NOTE WE'VE CHANGED DATA TO JSON
content = requests.get(url = endpoint, headers = header)

# show the status code, want 200
content.status_code
data = content.json()
print(content.json())

try:
	order_id = data[0]['savedOrderId']
	print(order_id)

except:
	print("There are no orders queued at this time.")

finally:
	time.sleep(3)
	print("Now exiting.")