import datetime
import discord
import urllib
import requests
from splinter import Browser
from selenium import webdriver
import sys
import os
import splinter
import asyncio
import json
import time
from ruamel.yaml import YAML
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from qasync import QEventLoop, asyncSlot
from window import Ui_MainWindow
import Order_Files.ordermodule as ordermod

yaml = YAML()

with open("./Config_Files/YAML/main_channel_id.yml", "r", encoding = "utf-8") as file:
        mainchannel = yaml.load(file)

class MyClient(discord.Client):
    async def on_connect(self):
        print(">>>>CONNECTING TO DISCORD")

    async def on_ready(self):
        # Channel ID
        main_channel_id = int(mainchannel["Main Channel ID"])

        # Embedded Message Colors
        self.embed_green = discord.Color.from_rgb(37, 225, 45)
        self.embed_red = discord.Color.from_rgb(255, 0, 0)
        self.embed_white = discord.Color.from_rgb(255, 250, 250)
        self.embed_black = discord.Color.from_rgb( 0, 0, 0)
        self.embed_lightblue = discord.Color.from_rgb(0, 175, 225)

        with open("./Config_Files/YAML/embed_settings.yml", "r", encoding = "utf-8") as file:
            embedsettings = yaml.load(file) 

        # Embedded Message Properties
        self.footer_text = embedsettings["Embed Settings"]["Footer"]["Text"]
        self.bull_icon = embedsettings["Embed Settings"]["Footer"]["Icon URL"]
        print(f"I am logged in as {self.user} and connected to Discord! ID: {self.user.id}")
        game = discord.Game(name = "Checking Orders!")
        await self.change_presence(activity = game)
        self.main_channel = self.get_channel(main_channel_id)
        print('-----')
        main_loop = True
        print(">>>>> Hello! Now starting Authentication process.")
        
        async def auth_api(self):

          yaml = YAML()

          with open("./Config_Files/YAML/config.yml", "r", encoding = "utf-8") as file:
            template = yaml.load(file)

          # define path to chrome driver
          executable_path = {'executable_path':r'C:\Users\Bryan Castillo\Desktop\chromedriver'}

          # Set some default behaviors for browser
          #options = webdriver.ChromeOptions()

          # make sure window is maximized
          #options.add_argument("--start-maximized")

          # make sure notifications are off
          #options.add_argument("--disable-notifications")

          # create a new browser object by default it is firefox
          browser = Browser('chrome', 
                          **executable_path, 
                          headless = True
                          #,options = options
                          )

          # define the components of the url
          method = 'GET'
          url = 'https://auth.tdameritrade.com/auth?'
          client_code = template["TDA_client_ID"] + '@AMER.OAUTHAP'
          payload = {'response_type':'code', 'redirect_uri':'http://localhost', 'client_id':client_code}

          # build the url
          built_url = requests.Request(method, url, params = payload).prepare()
          built_url = built_url.url

          # go to url
          browser.visit(built_url)

          # define elements to pass through form
          payload = {'username':template["TDA_username"], 
                     'password':template["TDA_password"]}

          ### LOGIN ELEMENT ###
          # find the username element and input
          browser.find_by_id("username0").first.fill(payload['username'])
          
          # find the password element and input
          try:
            browser.find_by_id("password1").first.fill(payload['password'])
          except splinter.exceptions.ElementDoesNotExist:
            browser.find_by_id("password").first.fill(payload['password'])
          finally:
            browser.find_by_id("accept").first.click()

          # Click the ccant get text message link
          browser.find_by_text('Can\'t get the text message?').first.click()

          # Get the Answer Box
          browser.find_by_value("Answer a security question").first.click()

          # Accept terms and conditions button
          try:
            browser.find_by_id("accept").first.click()
          except splinter.exceptions.ElementDoesNotExist:
            pass
          finally:
            print("Confirm button does not exist, skipping 'press confirm button'.")

          # Answer the Security Questions.
          try:
            if browser.is_text_present('What is the name of the first company you worked for?'):
              browser.find_by_id('secretquestion0').first.fill('dad')

            elif browser.is_text_present('What is your best friend\'s first name?'):
              browser.find_by_id('secretquestion0').first.fill('austin')

            elif browser.is_text_present('What was the name of your first pet?'):
              browser.find_by_id('secretquestion0').first.fill('ruffis')

            elif browser.is_text_present("Where did you meet your spouse for the first time? (Enter full name of city only.)"):
              browser.find_by_id('secretquestion0').first.fill('San Jose')
          except:
            print("The questions or answers were typed incorrectly here.")
          finally:
            print("Security Question Answered.")
          
          # submit results
          browser.find_by_id("accept").first.click()

          #Trust this device
          browser.find_by_xpath('/html/body/form/main/fieldset/div/div[1]/label').first.click()
          browser.find_by_id('accept').first.click()

          # click allow on last page
          browser.find_by_id("accept").first.click()
          time.sleep(1)

          # grab the url and parse it
          new_url = browser.url
          parse_url = urllib.parse.unquote(new_url.split('code=')[1])

          # close the browser
          browser.quit()
          print("URL HAS BEEN PARSED.")

          # define the endpoint
          url = r'https://api.tdameritrade.com/v1/oauth2/token'

          # define the headers
          headers = {'Content-Type':"application/x-www-form-urlencoded"}

          # define the payload
          payload = {'grant_type':'authorization_code',
                     'acccess_type':'offline',
                     'code':parse_url,
                     'client_id':template["TDA_client_ID"],
                     'redirect_uri':'http://localhost'}

          # post the data to get the token
          authReply = requests.post(url, headers = headers, data = payload)

          # convert json string to dictionary
          decoded_content = authReply.json()
          print("CONTENT DECODED.")

          # export data to a json file
          with open('./tokens/tokens.json' , 'w') as json_file:
            json.dump(decoded_content,json_file)

        await auth_api(self)

        async def get_orders(self):
            print("-----")
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

            await get_orders(self)
                    
            async def order_read(self):
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
                                    color = self.embed_green,
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
                                    color = self.embed_lightblue,
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
                                color = self.embed_red,
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
                            text = self.footer_text,
                            icon_url = self.bull_icon)

                            if order_template not in ordermod.sent_orders:
                                ordermod.sent_orders.append(order_template)
                                await self.main_channel.send(f"{order_template} @everyone", embed=embed)
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

            await order_read(self)

            if order_grab == False:
                print("-----")
                print("Now re-grabbing API Key.")

    async def on_resumed(self):
        print("Bot has returned to session")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send(f"Client Latency: {round(self.latency * 1000)}")

    async def on_disconnect(self):
        print("Bot Offline")

class Stream(QtCore.QObject):
    newText = QtCore.pyqtSignal(str)

    @QtCore.pyqtSlot(str)
    def write(self, text):
        self.newText.emit(str(text))

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    newText = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.client = MyClient()
        self.run_button.clicked.connect(self.on_clicked)
        self.close_button.clicked.connect(self.close)
        self.submit_button.setEnabled(False)
        self.discord_channel_line.textChanged.connect(self.disableButton)
        self.submit_button.clicked.connect(self.save_info)
        sys.stdout = Stream(newText=self.onUpdateText)

    @asyncSlot()
    async def on_clicked(self):
        await self.client.start(#ENTER DISCORD CHANNEL ID HERE IN QUOTES)

    def disableButton(self):
        if len(self.discord_channel_line.text()) > 0:
            self.submit_button.setEnabled(True)

    def save_info(self):
        yaml = YAML()
        data1 = {"TDA_client_ID": (self.TDA_client_ID_line.text()),
        "TDA_account_num": (self.TDA_account_num_line.text()),
        "TDA_username": (self.TDA_username_line.text()),
        "TDA_password": (self.TDA_password_line.text())}
        
        with open("./Config_Files/YAML/config.yml", "w", encoding = "utf-8") as file1:
            yaml.dump(data1, file1)

        data2 = {"Main Channel ID": (self.discord_channel_line.text())}

        with open("./Config_Files/YAML/main_channel_id.yml", "w", encoding = "utf-8") as file2:
            yaml.dump(data2, file2)

    @QtCore.pyqtSlot(str)
    def onUpdateText(self, text):
        cursor = self.terminal_box.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.terminal_box.setTextCursor(cursor)
        self.terminal_box.ensureCursorVisible()

    def __del__(self):
        sys.stdout = sys.__stdout__

def windowLauncher():
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    win = MainWindow()
    win.show()
    loop.run_forever()

if __name__ == "__main__":
    windowLauncher()
