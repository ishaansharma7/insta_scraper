from pprint import pprint
from time import sleep
import traceback
from data.one_time_insta_login import do_insta_login
from flask import current_app
import pandas as pd
import random
from utils.exist_check import check_handle_valid, user_handle_pvt
from utils.read_from_html import get_reel_details, get_user_details, get_shortcodes, get_upload_dates
from constants import CONSECUTIVE_FAIL_LIMIT, SELENIUM_FAIL_LIMIT, CRED_AVAILABLE, USER_NAME, PASSWORD, CHROMEDRIVER, HEADLESS, REUSE_SESSION, BATCH_SIZE
import requests
import json
from data.send_data_to_apis import request_scraping_creds, return_status_resp, reels_data_to_api, user_data_to_api, get_user_name_batch
from utils.selenium_driver import get_web_driver
from utils.exist_check import check_if_logged_in


def health_check(consecutive_fail_ct, selenium_fail_ct):
    if consecutive_fail_ct >= CONSECUTIVE_FAIL_LIMIT:
        print('scraping id banned-------')
        return 'scraping id banned'
    if selenium_fail_ct >= SELENIUM_FAIL_LIMIT:
        print('selenium code break-------')
        return 'selenium code break'
    return None


def retry_login(scraping_id, password):
    print('login not present-----')
    print('retrying login-----')
    login_success, driver = do_insta_login(scraping_id, password)
    if not login_success:
        print('login failed exiting------')
        return
    return driver



def process_posts(batch=None):

    ###################### login id and password ######################
    if CRED_AVAILABLE:
        scraping_id, password = USER_NAME, PASSWORD
    else:
        scraping_id, password = request_scraping_creds()
    if not scraping_id or not password:
        print('problem in fetching scrape id creds, exiting-----')
        return
    
    ###################### session usage ######################
    if REUSE_SESSION:
        driver = get_web_driver(CHROMEDRIVER, HEADLESS)
        login_success = check_if_logged_in(driver)
    else:
        login_success, driver = do_insta_login(scraping_id, password)

    if not login_success:
        print('login failed, retrying------')
        scraping_id, password = request_scraping_creds()
        login_success, driver = do_insta_login(scraping_id, password)

    if not login_success:
        print('login failed, exiting------')
        return
        
    print('scraping id in use-----', scraping_id)
    ###################### get batch ######################
    if not batch:
        batch = get_user_name_batch(BATCH_SIZE)
        if not batch:
            print('problem in getting batch-----')
            return
    
    ###################### variables ######################
    user_name_status = {k: {'status': 'not_scraped', 'reason': 'scraping not started'} for k, v in batch.items()}
    failed_scrape_list = []
    consecutive_fail_ct = 0     # help to identify scraping ID banned or not
    selenium_fail_ct = 0        # help to identify selenium code break
    scraping_id_status = {'scrape_id': scraping_id, 'status': 'in_use'}
    response = {'batch_status': user_name_status, 'scraping_id_status': scraping_id_status, }

    curr_num = 1
    for user_name, user_id in batch.items():
        print('**********************************************')
        print(f'currently on number {curr_num} -----')
        curr_num += 1
        ###################### health check process ######################
        curr_health = health_check(consecutive_fail_ct, selenium_fail_ct)
        if curr_health:
            if curr_health == 'scraping id banned':
                print('banned id-----', scraping_id)
                driver.quit()
                consecutive_fail_ct = 0
                failed_scrape_list.clear()
                scraping_id, password = request_scraping_creds(False, scraping_id, 'banned')
                if not scraping_id or not password:
                    print('problem in fetching scrape id creds, exiting-----')
                    return_status_resp(user_name_status, scraping_id_status)
                    return
                login_success, driver = do_insta_login(scraping_id, password)
                if not login_success:
                    print('login failed exiting------')
                    return_status_resp(user_name_status, scraping_id_status)
                    return
                print('new scraping id-----', scraping_id)
                scraping_id_status['scrape_id'] = scraping_id
                scraping_id_status['status'] = 'in_use'
            elif curr_health == 'selenium code break':
                print('selenium code break-------')
                return_status_resp(user_name_status, scraping_id_status)
                return

        ###################### pd dataframe ######################
        media_df = pd.DataFrame(columns=["user_name", "media_url", "shortcode", "comments_count", "like_count", "view_count", "user_id"])
        print(user_name, user_id)

        wait_time = random.randrange(3, 7)
        sleep(wait_time)

        driver.get("https://www.instagram.com/{user_name}/".format(user_name=user_name))

        wait_time = random.randrange(3, 5)
        sleep(wait_time)
        
        ###################### checking account ######################
        if not check_handle_valid(driver):
            failed_scrape_list.append(user_name)
            consecutive_fail_ct += 1
            user_name_status.update({user_name:{'status': 'failed', 'reason': 'user name changed'}})
            return_status_resp({user_name:user_name_status[user_name]})
            print('skipping further process------')
            continue
        else:
            consecutive_fail_ct = 0
        #     user_name_status.update(**{k: {'status': 'failed', 'reason': 'user name changed'} for k in failed_scrape_list})
        #     failed_scrape_list.clear()
        user_pvt = user_handle_pvt(driver)

        # try:
        #     user_df = get_user_details(driver, user_name, user_id, user_pvt)
        #     user_data_to_api(user_df)
        #     user_df.to_excel(user_name + "_details.xlsx", encoding='utf-8', index=False)
        # except Exception as e:
        #     print(e)
        #     pass

        if user_pvt:
            user_name_status.update({user_name: {'status': 'scraped', 'reason': 'private account'}})
            return_status_resp({user_name:user_name_status[user_name]})
            print('skipping further process------')
            continue

        get_upload_dates(driver)
        
        
        # here add the db code
        # reels_data_to_api(media_df)
        # return_status_resp({user_name:user_name_status[user_name]})
        wait_time = random.randrange(3, 7)
        sleep(wait_time)
    print('short_codes-----')
    
    scraping_id_status['status'] = 'free'
    # return_status_resp(user_name_status, scraping_id_status)
    return 'batch scraping completed----'