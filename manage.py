from datetime import datetime, timedelta
from flask import current_app
from main import create_app
application = create_app()
import time
from scripts.test_script import hello_world
from data import process_batch
from kafka import KafkaConsumer
import json
import traceback
from scripts.kafka_producer import send_to_insta_kafka
from constants import BATCH_SIZE, CHROMEDRIVER, HEADLESS, CRED_AVAILABLE, USER_NAME, PASSWORD
from utils.selenium_driver import get_web_driver
from time import sleep, time
from datetime import timedelta
from data.highlights_data import get_high_data
from utils.read_from_html import per_hover
from data.scrape_posts import process_posts

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
   # process_posts(driver, 'beerbiceps', '', {}, {})
   sleep(5)
   return


@application.cli.command('process_reels')
def process_reels_func():
   batch = None
   batch = {
# "fairy_evanna" : "",
# "dilipsingh" : "",
# "vindujarenjith" : "",
# "shikhasuren" : "",
# "swati.0007_" : "78f277c7463f4e31925284f7baf5d9eb",
# "sreeramreddyvanga" : "",
# "i.nehavyas" : "eaf1460f729b4f79906823da1f7f2e8d",
# "seemasahu_2210" : "88cd90f40b3f41a2bd217787d703b471",
# "heenasahu409" : "",
# "teju_kamble1110" : "0fffa68b507946788ce3a5715f5de2a4",
# "advaitnikam279" : "88d5006bec3c49d9bb770b469f01ea6f",
# "mulwaniaiy" : "",
# "durga.malleswari.334" : "d2cb14e1ba8a405a87015bfce52e01d3",
# "maheriya_dipesh___3103" : "",
# "cutie.ginny" : "",
# "surbhijain2589" : "1fde46ee0cc54be7a3de01df4362b830",
# "sonaliuikey" : "",
# "dhyaara_agarwal" : "",
# "riyachauhan733" : "",
# "official_nikitasurve" : "72a4ee01c07c41fc8379df26ce3455b9",
# "priya_precious8816" : "",
# "nirajkumarpk3" : "",
# "firdausashraf03" : "",
# "riteshmee" : "",
# "pokemaggs" : "56789447b7214bdab8aa5dda2ee83fcc",
# "elegance_storekas" : "02e3b28a6835406fb923f79f13573052",
# "dr.aakash_nandan_" : "",
# "_mr_offline_king" : "",
# "siva_keerthi9849" : "",
# "neelamojha03" : "",
# "mom_dadandme.2" : "",
# "the_bengali_entertainers" : "496168619ac24f338f2e60960ff7b27c",
# "crystal_abhijit_" : "",
# "divyashrisondur" : "499f29fd1e3c4b9fa72d79268db1b32c",
# "sunshine_p_7" : "3b451f01eb3a409b9ca35e2f65e49b6c",
# "kanikatekwani" : "e222ca8d2b8343248f172f53916b55c2",
# "ssony9864" : "2829be5a7377420ab36dab4225413375",
# "makeoversbyjyotsnarohit" : "b9e3d5dfb62b4cd596525c3cc331a10c",
# "vassuvathsala" : "72acce2fcb754145b3b416bd490b5eaa",
# "sshar9107" : "0c81520cf1184ab2815fdc084aae4968",
# "naman.arora.16" : "",
# "maggies_magic_yt" : "b42e37339fca46b2b04bce3c5a8f3bcb",
# "not_your_typical_foodblogger_" : "",
# "pompyy2k@gmail.com" : "906569b51abd4f4682e3f3f85877c91e",
# "david_vma1208" : "",
# "naynikarajput" : "",
# "ronakraksha" : "",
# "hopefull_him" : "",
# "_official_akku_baniya_" : "",
# "krsnk_a" : "53f8584a07fd4a3f8c66c956cea4e811",
'round2hell':''
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