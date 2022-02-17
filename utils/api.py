from flask import Flask
import requests

class API():

	def __init__(self, endpoint, headers=None):
		self.baseUrl = endpoint
		self.headers = {'Content-Type': 'application/json'}
		if headers:
			c_headers = self.headers.copy()
			c_headers.update(headers)
			self.headers = c_headers

	def add_header(self, header, value):
		self.headers[header] = value

	def get(self, endpoint, data=None):
		if data:
			res = requests.get("".join([self.baseUrl, endpoint]), headers=self.headers, json=data)
		else:
			res = requests.get("".join([self.baseUrl, endpoint]), headers=self.headers)
		if res.status_code != 200:
			raise Exception("UA001", "Api error")
		else:
			content_type = res.headers.get('Content-Type', None)
			if content_type and "application/json" in content_type:
				response = res.json()
				if "status" in response:
					if response["status"] == "success" and response["data"]:
						return response["data"]["result"]
					else:
						raise Exception("UA002", response["reason"])
				else:
					return response

			else:
				return res.text
		return ""

	def post(self, endpoint, data):
		res = requests.post("".join([self.baseUrl, endpoint]), headers=self.headers, json=data)
		if res.status_code != 200:
			raise Exception("UA003", "Api error")
		else:
			content_type = res.headers.get('Content-Type', None)
			if content_type and "application/json" in content_type:
				response = res.json()
				if response["status"] == "success" and response["data"]:
					return response["data"]["result"]
				else:
					raise Exception("UA004", response["reason"])
			else:
				return res.text
		return ""

	def patch(self, endpoint, data):
		res = requests.patch("".join([self.baseUrl, endpoint]), headers=self.headers, json=data)
		if res.status_code != 200:
			if res.status_code == 400:
				json_error_response = res.json()
				if json_error_response and "reason" in json_error_response:
					raise Exception("UA005", json_error_response["reason"])
			else:
				raise Exception("UA005", "Api error")
		else:
			content_type = res.headers.get('Content-Type', None)
			if content_type and "application/json" in content_type:
				response = res.json()
				if response["status"] == "success" and response["data"]:
					return response["data"]["result"]
				else:
					raise Exception("UA006", response["reason"])
			else:
				return res.text
		return ""

	def put(self, endpoint, data):
		print("".join([self.baseUrl, endpoint]), self.headers, data)
		res = requests.put("".join([self.baseUrl, endpoint]), headers=self.headers, json=data)
		if res.status_code != 200:
			raise Exception("UA007", "Api error")
		else:
			content_type = res.headers.get('Content-Type', None)
			if content_type and "application/json" in content_type:
				response = res.json()
				if response["status"] == "success" and response["data"]:
					return response["data"]["result"]
				else:
					raise Exception("UA008", response["reason"])
			else:
				return res.text
		return ""
