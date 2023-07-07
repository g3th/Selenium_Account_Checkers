import time

# import requestium
# from requestium import Session, Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def selenium_requests():

	heads = {'Connection': 'keep-alive',
			  'Server': 'nginx',
			  'Content-Type': 'text/html; charset=utf-8',
			  'Cache-Control': 'no-cache',
			  'X-Frame-Options': 'SAMEORIGIN',
			  'Set-Cookie': 'ovvuid=bb7470a9-4e85-4863-b551-8667ea62be6c; '
							'path=/, ovvuid=bb7470a9-4e85-4863-b551-8667ea62be6c; '
							'path=/',
			  'Content-Encoding': 'gzip',
			  'X-Real-Server': 'us_www_web_prod_vip1',
			  'Age': '0',
			  'Accept-Ranges': 'bytes',
			  'X-Origin-Cache': 'MISS',
			  'X-Origin-Hit-Count': '0',
			  'Via': '1.1 www-cache-545f699fc4-wgffh (Varnish/7.2), 1.1 google, 1.1 varnish, 1.1 varnish',
			  'Date': '',
			  'Vary': 'Accept-Encoding',
			  'X-CDN-Cache-Hits': '0',
			  'X-CDN-Cache': 'MISS',
			  'X-CDN-Timer': 'S1688707106.430599,VS0,VE112',
			  'X-CDN-Served-By': 'cache-iad-kiad7000170-IAD',
			  'transfer-encoding': 'chunked',
			 'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36'}

	browser = webdriver.Chrome()
	#s = Session(webdriver_path='/home/chromedriver', default_timeout=15)
	browser.get("https://www.paramountplus.com/account/signin/")
	#s.get("https://www.paramountplus.com/account/signin/", headers=heads)
	#s.transfer_session_cookies_to_driver()
	time.sleep(600)


def connection_error():
	page = 'https://www.paramountplus.com/account/signin/'

	browser = webdriver.Chrome()
	browser.set_window_size(500, 600)
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
		raise ConnectionError('Error')
