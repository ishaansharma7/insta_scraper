from datetime import datetime, timedelta
from flask import current_app
from main import create_app
application = create_app()
import time
from scripts.test_script import hello_world
from data import process_batch
from data import process_posts
from kafka import KafkaConsumer
import json
import traceback
from scripts.kafka_producer import send_to_insta_kafka
from constants import BATCH_SIZE, CHROMEDRIVER, HEADLESS, CRED_AVAILABLE, USER_NAME, PASSWORD
from utils.selenium_driver import get_web_driver
from time import sleep, time
from datetime import timedelta
from data.highlights_data import get_high_data
from utils.read_from_html import get_upload_dates
from utils.mymoney_db import get_new_users
from utils.fb_apis import get_user_details_from_api, get_details_from_response
from utils.utils import user_details_from_api_scrapper

@application.cli.command('test_cmd')
def func_test_cmd():
   hello_world()


@application.cli.command('user_details')
def user_details():
   if CRED_AVAILABLE:
      scraping_id, password = USER_NAME, PASSWORD
   else:
      print('no creds for login-----')
      return
   driver = get_web_driver(CHROMEDRIVER, False)
   # _, driver = do_insta_login(scraping_id, password)
   get_upload_dates(driver)
   sleep(5)
   return


@application.cli.command('process_reels')
def process_reels_func():
   batch = None
   # batch = {
   #    # 'sani_singh_41': '',
   #    # 'rohan.bajwa97': '',
   #    # 'i_am_srk_2': '',
   #    # 'fan_aewdon': '',
   #    'anuj.suman': '',
   #    }
   print('start time-----',datetime.now())
   start_epoch = time()

   print(process_batch.start_batch_processing(batch))

   print('end time-----',datetime.now())
   end_seconds = time() - start_epoch
   print('total duration-----', timedelta(seconds=end_seconds))
   print('\n \n \n')
   return

@application.cli.command('process_posts')
def process_posts_func():
   batch = None
   batch = {
      # 'sani_singh_41': '',
      # 'rohan.bajwa97': '',
      # 'i_am_srk_2': '',
      # 'fan_aewdon': '',
      'cristiano': '',
      }
   print('start time-----',datetime.now())
   start_epoch = time()

   print(process_posts.process_posts(batch))

   print('end time-----',datetime.now())
   end_seconds = time() - start_epoch
   print('total duration-----', timedelta(seconds=end_seconds))
   print('\n \n \n')
   return



@application.cli.command("consume_kafka")
def func_comment_sync_kafka():
   print("KAFKA CONSUMER CALLED")
   try:
      consumer = KafkaConsumer(bootstrap_servers= current_app.config['KAFKA_SERVER'], consumer_timeout_ms=1500, auto_offset_reset='earliest', enable_auto_commit=True, group_id = 'insta_scrapers')
      consumer.subscribe(current_app.config['KAFKA_USER_UPDATE_EVENT'])
      while True:
         for msg in consumer:
            msg = msg[6]
            payload = json.loads(msg)
            #callback_data = payload['payload']
            print('insta data: ', payload)
            # process_fb_callback(payload)
   except Exception as e:
      print ("Error in readFromKafka {}".format(e))
      traceback.print_exc()


@application.cli.command('produce_kafka')
def produce_kafka():
   send_to_insta_kafka({'name': 'ishaan', 'age': 99}, "2")
   print('worked')


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