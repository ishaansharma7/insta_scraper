from datetime import datetime, timedelta
from flask import current_app
from main import create_app
import os
application = create_app()
import time
from scripts.test_script import hello_world
from data import one_time_insta_login


@application.cli.command('test_cmd')
def func_test_cmd():
   hello_world()

@application.cli.command('insta_login')
def insta_login():
   one_time_insta_login.do_insta_login()
   return