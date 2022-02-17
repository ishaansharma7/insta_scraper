from flask import Flask, current_app
import json
import os
import traceback

from utils.api import API
from extensions import dbt
import requests

	
def get_user_data(user_id, user_token):
	try:
		req = API(current_app.config["API_BASE_URL"])
		req.add_header("id", user_id)
		req.add_header("mc4ktoken", user_token)
		user_info = req.get('/v1/users/' + user_id)
	except Exception as e:
		user_info = None
		traceback.print_exc()
		print(e)
	return user_info
