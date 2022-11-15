from datetime import datetime, timedelta
from main import create_app
from flask import current_app
import time
import traceback
import json
from kafka import KafkaConsumer
from scripts.test_script import hello_world
from data import process_batch
from constants import CHROMEDRIVER, CRED_AVAILABLE, USER_NAME, PASSWORD
from utils.selenium_driver import get_web_driver
from time import sleep, time
from datetime import timedelta
from utils.read_from_html import per_hover, get_single_reel_detail
from utils.exist_check import login_maintained_check
from utils.mymoney_db import get_new_users
from utils.fb_apis import get_user_details_from_api, get_details_from_response
from utils.utils import user_details_from_api_scrapper


application = create_app()


@application.cli.command('test_cmd')
def func_test_cmd():
   hello_world()


@application.cli.command('test_feature')
def user_details():
   if CRED_AVAILABLE:
      scraping_id, password = USER_NAME, PASSWORD
   else:
      print('no creds for login-----')
      return
   driver = get_web_driver(CHROMEDRIVER, False)
   # _, driver = do_insta_login(scraping_id, password)
   # get_single_date(driver, 'https://www.instagram.com/reel/Cj-GcxTgBTn/')
   # get_single_reel_detail(driver, 'https://www.instagram.com/reel/Cj-MVhAJA5y/')
   # driver.get('https://www.instagram.com/flying_kudi/')
   # per_hover(driver,{}, {'ct':0}, '', '')
   sleep(10)
   driver.get('https://www.instagram.com/harshbeniwal/')
   print(login_maintained_check(driver))
   sleep(300)
   return


@application.cli.command('process_batch')
def process_batch_func():
   batch = None
   batch = {
      
   }
   print('start time-----',datetime.now())
   start_epoch = time()

   print(process_batch.start_batch_processing(batch))

   print('end time-----',datetime.now())
   end_seconds = time() - start_epoch
   print('total duration-----', timedelta(seconds=end_seconds))
   print('\n \n \n')
   return


@application.cli.command('bulk_new_user_onboarding')
def new_user_onboarding(new_users=None):
   new_users = get_new_users()
   for user in new_users:
      print({user.get("acc_name", None) : user.get("user_id", "")})
      response = get_user_details_from_api(user)
      if response:
         get_details_from_response(user, response)
      else:
         process_batch.start_batch_processing({user.get("acc_name") : user.get("user_id")})


@application.cli.command("mymoney_insta_onboarding")
def func_comment_sync_kafka():
   try:
      consumer = KafkaConsumer(bootstrap_servers= current_app.config['KAFKA_SERVER'], consumer_timeout_ms=1500, auto_offset_reset='latest', enable_auto_commit=True, group_id = 'insta_onboarding')
      consumer.subscribe(current_app.config['KAFKA_INSTA_ONOARDING_EVENT'])
      while True:
         for msg in consumer:
            msg = msg[6]
            payload = json.loads(msg)
            payload = payload.get("payload", {})
            user_details_from_api_scrapper(payload)
   except Exception as e:
      traceback.print_exc()
      print ("Error in readFromKafka {}".format(e))
