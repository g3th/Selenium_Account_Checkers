import time
from selenium import webdriver

page = 'https://www.paramountplus.com/account/signin/'

browser = webdriver.Chrome()
browser.set_window_size(500,600)
browser.get(page)

email_input_box = browser.find_element_by_xpath('//*[@id="email"]')
password_input_box = browser.find_element_by_xpath('//*[@id="password"]')
sign_in_button = browser.find_element_by_xpath('//*[@id="sign-in-form"]/div/div[3]/button')			
email_input_box.send_keys('dummy@email.com')
password_input_box.send_keys('MySecret123')
time.sleep(2)

if browser.find_elements_by_xpath('//*[@id="recaptcha-anchor-label"]'):
	print('Captcha found.')
	exit()
else:
	raise ConnectionError ('Error')

