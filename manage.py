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
from utils.read_from_html import get_single_date, per_hover


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
   # get_single_date(driver, 'https://www.instagram.com/reel/Cj-GcxTgBTn/')
   per_hover(driver)
   sleep(5)
   return


@application.cli.command('process_reels')
def process_reels_func():
   batch = None
   batch = {
      'cristiano':''
      }
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