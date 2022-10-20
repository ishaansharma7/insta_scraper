from datetime import datetime, timedelta
from pprint import pprint
from flask import current_app
from main import create_app
import os
application = create_app()
import time
from scripts.test_script import hello_world
from data import one_time_insta_login
from data import process_reels
from data.send_data_to_apis import get_user_name_batch
from kafka import KafkaConsumer
import json
import traceback
from scripts.kafka_producer import send_to_insta_kafka
import requests
from constants import BATCH_SIZE, CHROMEDRIVER, HEADLESS
from utils.selenium_driver import get_web_driver
from utils.exist_check import check_if_logged_in


@application.cli.command('test_cmd')
def func_test_cmd():
   hello_world()


@application.cli.command('login_check')
def insta_login():
   driver = get_web_driver(CHROMEDRIVER, HEADLESS)
   print(check_if_logged_in(driver))
   return


@application.cli.command('process_reels')
def process_reels_func():
   # batch = {'anushkasalunke_16': '', }
   print(process_reels.process_reels())
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