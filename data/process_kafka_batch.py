from time import sleep
from flask import current_app
from data.one_time_insta_login import do_insta_login
import random
import traceback
from utils.exist_check import check_handle_valid, user_handle_pvt, login_maintained_check, tell_current_sc_id
from utils.read_from_html import get_user_details
from utils.scraper_kafka import send_lost_users_to_kafka
from constants import CONSECUTIVE_FAIL_LIMIT, BATCH_SIZE
from data.send_data_to_apis import request_scraping_creds, fail_status_api, user_data_to_api, get_user_name_batch, update_scrape_id_status
from data.scrape_reels import process_reel
from data.scrape_posts import process_posts
from data.session_management import get_session
from kafka import KafkaConsumer
from data.find_user import process_invalid_username
import json


def health_good(health_vars):
    if health_vars['page_not_avail'] >= CONSECUTIVE_FAIL_LIMIT:
        print('scraping id banned-------')
        return False
    return True


def retry_login(driver):
    old_sc_id = tell_current_sc_id(driver)
    if old_sc_id:
        update_scrape_id_status(old_sc_id, 'banned')
    driver.close()
    print('maybe id banned, retrying login ------')
    try:
        # update_scrape_id_status(scraping_id, 'banned')
        scraping_id, password = request_scraping_creds()
        print('new scraping id:', scraping_id)
        login_success, driver = do_insta_login(scraping_id, password)

        if not login_success:
            print('login failed, exiting------')
            return None
        return driver
    except Exception:
        traceback.print_exc()
        print('failure in re-login process, POS:pb-2 ------')
    return None


def start_kafka_batch_processing():
    

    ###################### session usage ######################
    login_success, driver = get_session()
    if not login_success:
        print('login failed, exiting------')
        return
    # if not REUSE_SESSION:   print('scraping id in use-----', scraping_id)

    
    ###################### health variables ######################
    health_vars = {'page_not_avail':0, 'selenium_fail':0}
    
    ###################### process variables ######################
    lost_users_temp = {}
    lost_users_perm = {}


    ###################### batch processing starts ######################
    curr_num = 1
    consumer = KafkaConsumer(bootstrap_servers= current_app.config['KAFKA_SERVER'], consumer_timeout_ms=1500, auto_offset_reset='latest', group_id = 'test_group_id')
    consumer.subscribe(current_app.config['SCRAPER_KAFKA_TOPIC'])
    print('READY FOR CONSUMPTION -----')
    print('**********************************************')
    while True:
        for msg in consumer:
            # print("offset", msg.offset)
            msg = msg[6]
            payload = json.loads(msg)
            # print(payload)
            user_name = payload.get('user_name')
            user_id = payload.get('user_id')
            consumer.commit()
            if not user_name:
                continue
            try:
                user_name = user_name.lower()
                ###################### user variables ######################
                user_data_dict = {
                    'user_name': user_name,
                    'user_id': user_id,
                    'scrape_status': 'not_scraped',
                    'reason': []
                }
                print('**********************************************')
                print(f'currently on number {curr_num} -----')
                curr_num += 1

                print('current user_name:', user_name, user_id)

                wait_time = random.randrange(2, 5)
                sleep(wait_time)

                driver.get("https://www.instagram.com/{user_name}/".format(user_name=user_name))

                wait_time = random.randrange(2, 5)
                sleep(wait_time)

                ###################### health check process ######################
                if not login_maintained_check(driver) or not health_good(health_vars):
                    driver = retry_login(driver)
                    if not driver:  return
                    driver.get("https://www.instagram.com/{user_name}/".format(user_name=user_name))
                    health_vars['page_not_avail'] = 0
                    lost_users_perm.update(lost_users_temp)
                    send_lost_users_to_kafka(lost_users_perm)
                    lost_users_temp.clear()
                    wait_time = random.randrange(2, 5)
                    sleep(wait_time)
                
                ###################### checking account ######################
                if not check_handle_valid(driver):
                    found_user, new_user_name = process_invalid_username(driver, user_name)
                    if found_user:
                        user_name = new_user_name
                        user_data_dict['user_name'] = user_name
                        health_vars['page_not_avail'] = 0
                        lost_users_temp.clear()
                    else:
                        user_data_dict["scrape_status"] = 'failure'
                        user_data_dict["reason"] = []
                        user_data_dict["reason"].append('page_not_available')
                        fail_status_api(user_data_dict)
                        print('skipping further process------')
                        health_vars['page_not_avail'] += 1
                        lost_users_temp[user_name] = user_id
                        continue
                else:
                    health_vars['page_not_avail'] = 0
                    lost_users_temp.clear()

                ###################### scrape user info ######################
                user_pvt = user_handle_pvt(driver)
                try:
                    user_df, post_count = get_user_details(driver, user_name, user_id, user_pvt)
                    user_data_to_api(user_df)
                    user_df.to_excel('excel_dir/' + user_name + "_details.xlsx", encoding='utf-8', index=False)
                except Exception as e:
                    traceback.print_exc()
                    pass

                if user_pvt:
                    print('skipping further process------')
                    continue

                if post_count == 0:
                    print('no post-----')
                    continue
                
                ###################### processing reels ######################
                process_reel(driver, user_name, user_id)
                ###################### processing posts ######################
                process_posts(driver, user_name, user_id)

            except Exception:
                traceback.print_exc()
                user_data_dict["scrape_status"] = 'failure'
                user_data_dict["reason"] = []
                user_data_dict["reason"].append('selenium_failed')
                print(f'no details scraped for {user_name}, maybe a major process like details, reel or post scrape failed, POS:pb-1 ------')
                # fail_status_api(user_data_dict)
    print('batch scraping completed----')
    return