from ruamel.yaml import YAML
import time
import urllib
import requests
import json
from splinter import Browser
from selenium import webdriver

def auth_api():

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