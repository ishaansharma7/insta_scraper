from datetime import datetime, timedelta
from flask import current_app
from main import create_app
import os
application = create_app()
import time
from scripts.test_script import hello_world
from data import one_time_insta_login
from data import process_reels


@application.cli.command('test_cmd')
def func_test_cmd():
   hello_world()


@application.cli.command('insta_login')
def insta_login():
   USER_NAME = current_app.config['USER_NAME']
   PASSWORD = current_app.config['PASSWORD']
   one_time_insta_login.do_insta_login(USER_NAME, PASSWORD)
   return


@application.cli.command('process_reels')
def process_reels_func():
   batch = {
      "ee8a3f35ad4645e2b7892178a7f7d2cc" : "gudsaloni",
      "ee8c5ed8e82545698403a55c7678eff2" : "ripans_world",
      "eea64b19faab40cfbb2361ee76b74fe0" : "malhotrashyna40",
   }
   process_reels.process_reels(batch)
   return