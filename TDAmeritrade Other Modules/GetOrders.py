import time
import urllib
import requests
import json
import asyncio
from splinter import Browser
from selenium import webdriver
from config import client_id, username, password, account_number, account_ID
import AuthenticationAPI as authapi

main_loop = True

def get_orders():
	print("-----")
	print("Hello! Now starting Authorization process.")
	authapi.auth_api() 
	order_grab = True

	while order_grab == True:
		counter = 1
		print("-----")
		print("Now reading 'Tokens.json' file.")
		# load json file with tokens
		with open('tokens.json') as json_file:
			data = json.load(json_file)
			access_token = data["access_token"]

		while counter != 40 and order_grab == True:
			# define headers
			header = {'Authorization': "Bearer {}".format(access_token)}
			# define the endpoint for saved orders, including your account_ID
			endpoint = r"https://api.tdameritrade.com/v1/orders"
			# make a post, NOTE WE'VE CHANGED DATA TO JSON
			content = requests.get(url = endpoint, headers = header)

			print("-----")
			print("Now grabbing orders")
			# show the status code, want 200
			status = content.status_code
			print(f"STATUS CODE: {status}")

			data = content.json()
			with open('orders.json' , 'w') as json_file:
				json.dump(data,json_file)
			print("-----")
			print("You can find orders in 'orders.json'.")
			print(f">>COUNTER: {counter}")
			time.sleep(1)
			counter += 1
			
			if counter == 4:
				print("-----")
				print("Now re-grabbing API Key.")
				counter == 1
				order_grab = False
				break


while main_loop == True:
	print("-----")
	print(">>>>> RESTARTING LOOP")
	get_orders()