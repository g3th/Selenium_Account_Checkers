import json
import requests


class GenerateCookies:

	def __init__(self, page, directory, service):
		self.page = page
		self.directory = directory
		self.service = service
		self.headers = {}

	def create_headers(self):
		request = requests.get(self.page)
		unprepped_headers = dict(request.headers)
		for (k, v) in unprepped_headers.items():
			if "transfer-encoding" in k:
				pass
			else:
				self.headers[k] = v
		with open(self.directory + "/" + self.service + "_headers.json", 'w') as store_headers:
			json.dump(self.headers, store_headers, indent=3, sort_keys=True)

	def create_cookies(self):
		with requests.Session() as sesh:
			cookie_request = sesh.get(self.page, headers=self.headers)
			return dict(cookie_request.cookies)

