import asyncio
import json

def order_read():
	with open("orders.json") as json_file:
		data = json.load(json_file)
		order_info = data
		orderlegtype = order_info["orderLegCollection"]

		# quantity = order_info["quantity"]
		price = order_info["price"]
		symbol = orderlegtype[0]["instrument"]["underlyingSymbol"]
		
		# Order instruction
		instruction = orderlegtype[0]["instruction"]
		if instruction == "BUY_TO_OPEN":
			instruction = "BTO"
		elif instruction == "SELL_TO_CLOSE":
			instruction = "STC"

		raw_description = orderlegtype[0]["instrument"]["description"]
		description = raw_description.split()
		
		# Strike Price of contract
		raw_strike = description[4]
		if str(raw_strike).endswith(".0"):
			strike = raw_strike.split(".")
			strike = strike[0]
		else:
			strike = raw_strike
		
		# Option Call or Put
		option_type = description[5]
		if option_type == "Call":
			option_type = "C"
		elif option_type == "Put":
			option_type = "P"
		
		# Expiration of Contract
		exp_date = description[1] + description[2] + description[3]
		
		# Check to see if order was filled
		status = order_info["status"]
		
		# Timestamp
		raw_datetime = order_info["enteredTime"].split("T")
		raw_time = raw_datetime[1].split(":")
		hour = (int(raw_time[0]) - 8)
		if hour < 12:
			time = str(str(hour) + ':' + raw_time[1] + "am" + " PST")
		elif hour >= 12:
			time = str(str(hour) + ':' + raw_time[1] + "pm" + " PST")


		if status == "FILLED":
			# For debugging only
			'''
			print(f"SYMBOL: {symbol}")
			print(f"PRICE: {price}")
			print(instruction)
			print(f"{strike} STRIKE PRICE")
			print(f"{option_type}")
			print(f"EXP: {exp_date}")
			print(time)
			'''

			# So you know what was sent out
			order_template = str(instruction + " " + symbol + " " + exp_date + " " + strike + option_type + " " + " @" + str(price) + " " + time)
			print(order_template)

#order_read()