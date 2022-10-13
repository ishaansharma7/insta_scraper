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
from kafka import KafkaConsumer
import json
import traceback
from scripts.kafka_producer import send_to_insta_kafka


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
      # "ee8a3f35ad4645e2b7892178a7f7d2cc" : "gudsaloni",
      # "ee8c5ed8e82545698403a55c7678eff3" : "__anirudh.sharma__",
      # "ee8c5ed8e82545698403a55c7678eff2" : "ripans_world",
      # "11y": "anuj.suman",
      # "11a": "ishaansharma711",
      # "11b": "ishaansharma71a1",
      # "11x": "div._.ig",

      "11c": "ishaansharma71b1",
      "11d": "ishaansharma71c1",
      "11e": "ishaansharma71d1",
      "11f": "ishaansharma71e1",
      "11g": "ishaansharma71f1",
      "11h": "ishaansharma71g1",
      "eea64b19faab40cfbb2361ee76b74fe0" : "malhotrashyna40",
   }
   pprint(process_reels.process_reels(batch))
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
   send_to_insta_kafka({'name': 'ishaan', 'age': 99}, "69")
   print('worked')