import time
import urllib
import requests
from splinter import Browser
from selenium import webdriver
from config import client_id, username, password, account_number, access_token, account_ID

headers = {'Authorization': "Bearer {}".format(access_token)}
# ACCOUNTS ENDPOINT - Query for Accounts

# Define the Accounts Endpoint
endpoint = r"https://api.tdameritrade.com/v1/accounts/{}".format(account_ID)

# make a request
content = requests.get(url = endpoint, headers = headers)

# convert it dictionary object
data = content.json()
print(data)