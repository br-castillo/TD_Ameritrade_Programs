import datetime
import os
import splinter
import asyncio
import json
import time
from ruamel.yaml import YAML
import requests
import discord
import Order_Files.ordermodule as ordermod

yaml = YAML()
def order_sniper():
    with open("./Config_Files/YAML/main_channel_id.yml", "r", encoding = "utf-8") as file:
        mainchannel = yaml.load(file)    

    client = discord.Client()

    '''
    Bot Properties being read from Config.yml
    '''

    # Channel ID
    main_channel_id = int(mainchannel["Main Channel ID"])

    # Embedded Message Colors
    client.embed_green = discord.Color.from_rgb(37, 225, 45)
    client.embed_red = discord.Color.from_rgb(255, 0, 0)
    client.embed_white = discord.Color.from_rgb(255, 250, 250)
    client.embed_black = discord.Color.from_rgb( 0, 0, 0)
    client.embed_lightblue = discord.Color.from_rgb(0, 175, 225)

    with open("./Config_Files/YAML/embed_settings.yml", "r", encoding = "utf-8") as file:
        embedsettings = yaml.load(file) 

    # Embedded Message Properties
    client.footer_text = embedsettings["Embed Settings"]["Footer"]["Text"]
    client.bull_icon = embedsettings["Embed Settings"]["Footer"]["Icon URL"]

    '''
    Bot event on start-up
    '''

    @client.event
    async def on_ready():
        print(f"I am logged in as {client.user} and connected to Discord! ID: {client.user.id}")

        game = discord.Game(name = "Checking Orders!")
        await client.change_presence(activity = game)
        client.main_channel = client.get_channel(main_channel_id)
        print('-----')
        main_loop = True
        # sent_orders = []

        async def get_orders():
            print("-----")
            print(">> Hello! Now starting Authentication process.")
            import Authenticator.AuthenticationAPI as authapi
            authapi.auth_api() 
            order_grab = True

            while order_grab == True:
                print("-----")
                print(">> Now reading 'Tokens.json' file.")
                
                # load json file with tokens
                with open('./tokens/tokens.json') as json_file:
                    data = json.load(json_file)
                    access_token = data["access_token"]

                while order_grab == True:
                    # define headers
                    header = {'Authorization': "Bearer {}".format(access_token)}
                    # define the endpoint for saved orders, including your account_ID
                    endpoint = r"https://api.tdameritrade.com/v1/orders"
                    # make a post, NOTE WE'VE CHANGED DATA TO JSON
                    content = requests.get(url = endpoint, headers = header)

                    print("-----")
                    print(">> Now grabbing orders")
                    # show the status code, want 200
                    status = content.status_code
                    print(">>>> We want 'STATUS CODE' 200")
                    
                    if status == 200:
                        print(f">>>> YOUR STATUS CODE: {status}")
                    else:
                        print(f">>>> YOUR STATUS CODE CAME BACK AS {status}. A CONNECTION COULD NOT BE ESTABLISHED AT THIS TIME.")
                        order_grab = False
                        break

                    data = content.json()
                    with open('./Order_Files/orders/orders.json' , 'w') as json_file:
                        json.dump(data,json_file)
                    time.sleep(1)
                    
                    async def order_read():
                        with open("./Order_Files/orders/orders.json") as json_file:
                            data = json.load(json_file)
                            for order_info in data:
                                orderlegtype = order_info["orderLegCollection"]
                                asset_type = orderlegtype[0]["instrument"]["assetType"]
                                status = order_info["status"]
                                
                                if asset_type == "OPTION" and status == "FILLED":
                                    
                                    price = order_info["orderActivityCollection"][0]["executionLegs"][0]["price"]
                                    symbol = orderlegtype[0]["instrument"]["underlyingSymbol"]
                                    option_order = orderlegtype[0]["orderLegType"]
                                    order_id = order_info["orderId"]
                                    quantity = order_info["filledQuantity"]
                                
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
                                    try:
                                        option_type = description[5]
                                        if option_type == "Call":
                                            option_type = "C"
                                        elif option_type == "Put":
                                            option_type = "P"
                                    except IndexError:
                                        option_type = "?"
                                    
                                    # Expiration of Contract
                                    raw_exp_month = description[1]
                                    if raw_exp_month == "Jan":
                                        exp_month = "1/"
                                    elif raw_exp_month == "Feb":
                                        exp_month = "2/"
                                    elif raw_exp_month == "Mar":
                                        exp_month = "3/"
                                    elif raw_exp_month == "Apr":
                                        exp_month = "4/"
                                    elif raw_exp_month == "May":
                                        exp_month = "5/"
                                    elif raw_exp_month == "Jun":
                                        exp_month = "6/"
                                    elif raw_exp_month == "Jul":
                                        exp_month = "7/"
                                    elif raw_exp_month == "Aug":
                                        exp_month = "8/"
                                    elif raw_exp_month == "Sep":
                                        exp_month = "9/"
                                    elif raw_exp_month == "Oct":
                                        exp_month = "10/"
                                    elif raw_exp_month == "Nov":
                                        exp_month = "11/"
                                    elif raw_exp_month == "Dec":
                                        exp_month = "12/"

                                    exp_date = exp_month + description[2]
                                    
                                    # Check to see if order was filled
                                    status = order_info["status"]
                                    
                                    # Timestamp
                                    raw_datetime = order_info["enteredTime"].split("T")
                                    raw_time = raw_datetime[1].split(":")
                                    hour = (int(raw_time[0]) - 8)
                                    if hour < 12:
                                        timestamp = str(str(hour) + ':' + raw_time[1] + "am" + " PST")
                                    elif hour >= 12:
                                        timestamp = str(str(hour) + ':' + raw_time[1] + "pm" + " PST")

                                    # So you know what was sent out
                                    order_template = str(instruction + "   " + symbol + "  " + exp_date + "  " + strike + option_type + " " + " @ " + str(price) + "  " + timestamp)
                                    order_finder = str(symbol + " " + exp_date + " " + strike + option_type)

                                    if instruction == "BTO":
                                        if order_finder not in ordermod.open_orders:
                                            #totalQuantity = quantity
                                            #remainingQuantity = quantity
                                            ordermod.open_orders.update({order_finder : [instruction, symbol, exp_date, strike, option_type, price]})
                                            ordermod.open_times.update({order_finder : [hour, raw_time[1]]})
                                            #ordermod.open_filled.update({order_finder: [totalQuantity, remainingQuantity]})

                                            openorders = ordermod.open_orders
                                            opentimes = ordermod.open_times
                                            #openfilled = ordermod.open_filled
                                            with open("./Order_Files/orders/open_orders.json", "w") as json_file:
                                                json.dump([openorders, opentimes], json_file)
                                            
                                            embed = discord.Embed(
                                            title = order_template,
                                            color = client.embed_green,
                                            timestamp = datetime.datetime.now(datetime.timezone.utc)
                                            )

                                        elif order_finder in ordermod.open_orders:
                                            # for price difference
                                                # If you averaged down on a contract 
                                                # i.e. you bought another contract you already own
                                                # at a cheaper price, then P/L will be automatically
                                                # calculated including the average down :)
                                            average_price = (((price) + (ordermod.open_orders[order_finder][5]))/(2))
                                            
                                            embed = discord.Embed(
                                            title = order_template,
                                            color = client.embed_lightblue,
                                            description = f"``` Averaging down here, new price @ {round(average_price, 2)}```",
                                            timestamp = datetime.datetime.now(datetime.timezone.utc)
                                            )
                                            #totalQuantity = (ordermod.open_filled[order_finder][0] + quantity)
                                            #remainingQuantity = (ordermod.open_filled[order_finder][1] + quantity)
                                            price = average_price
                                            ordermod.open_orders.update({order_finder : [instruction, symbol, exp_date, strike, option_type, price]})
                                            #ordermod.open_filled.update({order_finder : [totalQuantity, remainingQuantity]})

                                            openorders = ordermod.open_orders
                                            opentimes = ordermod.open_times
                                            #openfilled = ordermod.open_filled
                                            with open("./Order_Files/orders/open_orders.json", "w") as json_file:
                                                json.dump([openorders, opentimes], json_file)

                                    elif instruction == "STC":
                                        if order_finder not in ordermod.open_orders:
                                            continue
                                        elif order_finder in ordermod.open_orders:
                                            ordermod.closed_orders.update({order_finder : [instruction, symbol, exp_date, strike, option_type, price]})
                                            ordermod.closed_times.update({order_finder : [hour, raw_time[1]]})
                                            #totalQuantity = quantity
                                            #remainingQuantity = (ordermod.open_filled[1] - quantity)
                                            #ordermod.closed_filled.update({order_finder: [totalQuantity, remainingQuantity]})
                                            #ordermod.open_filled.update({order_finder: [totalQuantity, remainingQuantity]})

                                            pl_percentage = ((((ordermod.closed_orders[order_finder][5]) - (ordermod.open_orders[order_finder][5]))/(ordermod.open_orders[order_finder][5]))*100)
                                            minutes_held = int(int(ordermod.closed_times[order_finder][1]) - int(ordermod.open_times[order_finder][1]))
                                            hours_held = int((int(ordermod.closed_times[order_finder][0])*60) - (int(ordermod.open_times[order_finder][0])*60))
                                            time_held = f"**{(hours_held) + (minutes_held)}**  minutes."

                                            
                                        if pl_percentage >= 0:
                                            sign = "+"
                                        else:
                                            sign = "-"
                                        
                                        '''
                                        if ordermod.open_filled[order_finder][1] == 0:
                                            if ordermod.open_orders.__contains__(order_finder):
                                                del ordermod.open_orders[order_finder]
                                                if ordermod.open_times.__contains__(order_finder):
                                                    del ordermod.open_times[order_finder]
                                                    if ordermod.open_filled.__contains__(order_finder):
                                                        del ordermod.open_filled[order_finder]
                                                    else:
                                                        pass
                                                else:
                                                    pass
                                            else:
                                                pass

                                        if ordermod.closed_filled[order_finder][1] == 0:
                                            if ordermod.closed_orders.__contains__(order_finder):
                                                del ordermod.closed_orders[order_finder]
                                                if ordermod.closed_times.__contains__(order_finder):
                                                    del ordermod.closed_times[order_finder]
                                                    if ordermod.closed_filled.__contains__(order_finder):
                                                        del ordermod.closed_filled[order_finder]
                                                    else:
                                                        pass
                                                else:
                                                    pass
                                            else:
                                                pass
                                        '''

                                        openorders = ordermod.open_orders
                                        opentimes = ordermod.open_times
                                        #openfilled = ordermod.open_filled (ADD IT BELOW)
                                        with open("./Order_Files/orders/open_orders.json", "w") as json_file:
                                            json.dump([openorders, opentimes], json_file)

                                        embed = discord.Embed(
                                        title = order_template,
                                        color = client.embed_red,
                                        timestamp = datetime.datetime.now(datetime.timezone.utc)
                                        )

                                        embed.add_field(
                                        name = "P/L %",
                                        value = (f"**{sign}{str(round(abs(pl_percentage), 2))} %**"),
                                        inline = True)

                                        embed.add_field(
                                        name = "Contracts Held For",
                                        value = f"{time_held}",
                                        inline = True)     
                                    
                                    else:
                                        print(f"{order_template} IS NOT A BTO OR STC OPTION ORDER, WILL SKIP.")
                                        continue

                                    embed.set_footer(
                                    text = client.footer_text,
                                    icon_url = client.bull_icon)

                                    if order_template not in ordermod.sent_orders:
                                        ordermod.sent_orders.append(order_template)
                                        await client.main_channel.send(f"{order_template} @everyone", embed=embed)
                                        print(f"Order '{order_template}' was sent successfully.")
                                        time.sleep(1)
                                        continue
                                    elif order_template in ordermod.sent_orders:
                                        print(f">>Order {order_template} already sent, skipping order.")
                                        time.sleep(1)
                                        continue

                                elif asset_type == "EQUITY":
                                    #quantity = order_info["quantity"]
                                    pass    

                    await order_read()

                    if order_grab == False:
                        print("-----")
                        print(f">>COUNTER: {counter}")
                        print("-----")
                        print("Now re-grabbing API Key.")
        
        while main_loop == True:
            print(">>>>> STARTING LOOP")
            await get_orders()

    client.run(#ENTER DISCORD CHANNEL ID HERE IN QUOTES)
