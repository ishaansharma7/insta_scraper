from datetime import datetime, timedelta
from main import create_app
application = create_app()
import time
from scripts.test_script import hello_world
from data import process_batch
from constants import CHROMEDRIVER, CRED_AVAILABLE, USER_NAME, PASSWORD
from utils.selenium_driver import get_web_driver
from time import sleep, time
from datetime import timedelta
from utils.read_from_html import per_hover

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
   # get_single_reel_detail(driver, 'https://www.instagram.com/reel/Cj94QgpjM8z/')
   per_hover(driver,{}, {'ct':0}, '', '')
   sleep(5)
   return


@application.cli.command('process_reels')
def process_reels_func():
   batch = None
   batch = {
      'cristiano':'',
   }
   print('start time-----',datetime.now())
   start_epoch = time()

   print(process_batch.start_batch_processing(batch))

   print('end time-----',datetime.now())
   end_seconds = time() - start_epoch
   print('total duration-----', timedelta(seconds=end_seconds))
   print('\n \n \n')
   return