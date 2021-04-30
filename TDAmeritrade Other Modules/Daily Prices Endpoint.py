import requests
from config import client_id

# The daily prices endpoint

# define our endpoint
endpoint = r"https://api.tdameritrade.com/v1/marketdata/{}/quotes".format('NIO')

# define our payload
payload = {'apikey':client_id}

# make a request
content = requests.get(url = endpoint, params = payload)

# convert it to a dicitonary
data = content.json()
print(data)