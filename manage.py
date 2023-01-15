from datetime import datetime, timedelta
from main import create_app
from flask import current_app
import time
import traceback
import json
from kafka import KafkaConsumer
from scripts.test_script import hello_world
from data import process_batch, process_kafka_batch
from constants import CHROMEDRIVER, CRED_AVAILABLE, USER_NAME, PASSWORD
from utils.selenium_driver import get_web_driver
from time import sleep, time
from datetime import timedelta
from utils.mymoney_db import get_new_users
from utils.fb_apis import get_user_details_from_api, get_details_from_response
from utils.utils import user_details_from_api_scrapper
import os
from utils.scraper_kafka import send_to_scraper_kafka
from data.find_user import find_new_user_name
from data.send_data_to_apis import get_shortcode_using_username


if not os.path.exists('excel_dir'):
   os.makedirs('excel_dir')

application = create_app()


@application.cli.command('test_cmd')
def func_test_cmd():
   hello_world()


@application.cli.command('test_feature')
def user_details():
   driver = get_web_driver(CHROMEDRIVER, False)
   sleep(10)
   find_new_user_name(driver, 'ishaan')
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



@application.cli.command("consume_batch")
def consume_batch():
   print('start time-----',datetime.now())
   start_epoch = time()

   print(process_kafka_batch.start_kafka_batch_processing())

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
            print("offset", msg.offset)
            msg = msg[6]
            payload = json.loads(msg)
            payload = payload.get("payload", {})
            print(payload.get("acc_name"))
            user_details_from_api_scrapper(payload)
            consumer.commit()
   except Exception as e:
      traceback.print_exc()
      print ("Error in readFromKafka {}".format(e))

@application.cli.command("test_kafka_con")
def test_kafka_con():
   try:
      consumer = KafkaConsumer(bootstrap_servers= current_app.config['KAFKA_SERVER'], consumer_timeout_ms=1500, auto_offset_reset='latest', group_id = 'test_group_id')
      consumer.subscribe(current_app.config['SCRAPER_KAFKA_TOPIC'])
      print(consumer)
      while True:
         for msg in consumer:
            print("offset", msg.offset)
            msg = msg[6]
            payload = json.loads(msg)
            print(payload)
            consumer.commit()
   except Exception as e:
      traceback.print_exc()
      print ("Error in readFromKafka {}".format(e))


@application.cli.command("send_to_kafka")
def test_kafka_pro():
   send_to_scraper_kafka({'user_name': '', 'user_id': ''})
   print('inserted username -----')

@application.cli.command("test_api")
def test_api():
   print(get_shortcode_using_username('ishaansharma711'))