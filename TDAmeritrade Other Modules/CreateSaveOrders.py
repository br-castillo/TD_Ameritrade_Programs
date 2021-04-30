import time
import urllib
import requests
from splinter import Browser
from selenium import webdriver
from config import client_id, username, password, account_number, access_token, account_ID

# define headers
header = {'Authorization': "Bearer {}".format(access_token),
          'Content-Type': 'application/json'}

# define the endpoint for saved orders, including your account_ID
endpoint = r"https://api.tdameritrade.com/v1/accounts/{}/savedorders".format(account_ID)

# define the payload, in JSON format
payload = {'orderType':'MARKET',
           'session': 'PM',
           'duration': 'DAY',
           'orderStrategyType':'SINGLE',
           'orderLegCollection':[{'instruction':'Sell',
                                  'quantity':1,
                                  'instrument':{'symbol':'PINS',
                                                'assetType':'EQUITY'}}]}
# make a post, NOTE WE'VE CHANGED DATA TO JSON
content = requests.post(url = endpoint, json = payload, headers = header)

# show the status code, want 200
print(content.status_code)