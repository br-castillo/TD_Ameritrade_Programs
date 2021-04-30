import time
import urllib
import requests
from splinter import Browser
from selenium import webdriver
from config import client_id, username, password, account_number, access_token

headers = {'Authorization': "Bearer {}".format(access_token)}
# ACCOUNTS ENDPOINT - Query for Accounts

# Define the Accounts Endpoint
endpoint = r"https://api.tdameritrade.com/v1/accounts"

# make a request
content = requests.get(url = endpoint, headers = headers)

# convert it dictionary object
data = content.json()
print(data)

account_id = data[0]['securitiesAccount']['accountId']
print(account_id)