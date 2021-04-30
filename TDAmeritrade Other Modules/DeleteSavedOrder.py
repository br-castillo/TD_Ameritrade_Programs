import time
import urllib
import requests
from splinter import Browser
from selenium import webdriver
from config import client_id, username, password, account_number, access_token, account_ID

# define headers
header = {'Authorization': "Bearer {}".format(access_token)}

savedOrderId = '15963144'
# define the endpoint for saved orders, including your account_ID
endpoint = r"https://api.tdameritrade.com/v1/accounts/{}/savedorders/{}".format(account_ID, savedOrderId)

# make a post, NOTE WE'VE CHANGED DATA TO JSON
content = requests.delete(url = endpoint, headers = header)

#show status code, we want 200
print(content.status_code)