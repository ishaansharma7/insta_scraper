from time import sleep
from data.one_time_insta_login import do_insta_login
import random
from utils.exist_check import check_handle_valid, user_handle_pvt
from utils.read_from_html import get_user_details
from constants import CONSECUTIVE_FAIL_LIMIT, SELENIUM_FAIL_LIMIT, CRED_AVAILABLE, USER_NAME, PASSWORD, CHROMEDRIVER, HEADLESS, REUSE_SESSION, BATCH_SIZE
from data.send_data_to_apis import request_scraping_creds, return_status_resp, user_data_to_api, get_user_name_batch
from utils.selenium_driver import get_web_driver
from utils.exist_check import check_if_logged_in
from data.scrape_reels import process_reel
from data.scrape_posts import process_posts


def health_check(health_vars):
    if health_vars['consecutive_fail_ct'] >= CONSECUTIVE_FAIL_LIMIT:
        print('scraping id banned-------')
        return 'scraping id banned'
    if health_vars['selenium_fail_ct'] >= SELENIUM_FAIL_LIMIT:
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

def health_check_process(health_vars):
    pass



def start_batch_processing(batch=None):

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
        
    if not REUSE_SESSION:   print('scraping id in use-----', scraping_id)
    ###################### get batch ######################
    if not batch:
        batch = get_user_name_batch(BATCH_SIZE)
        if not batch:
            print('problem in getting batch-----')
            return
    
    ###################### variables ######################
    user_name_status = {k: {'status': 'not_scraped', 'reason': 'scraping not started'} for k, v in batch.items()}
    failed_scrape_list = []
    health_vars = {}
    health_vars['consecutive_fail_ct'] = 0     # help to identify scraping ID banned or not
    health_vars['selenium_fail_ct'] = 0        # help to identify selenium code break
    scraping_id_status = {'scrape_id': scraping_id, 'status': 'in_use'}

    ###################### batch processing starts ######################
    curr_num = 1
    for user_name, user_id in batch.items():
        print('**********************************************')
        print(f'currently on number {curr_num} -----')
        curr_num += 1

        ###################### health check process ######################
        curr_health = health_check(health_vars)
        if curr_health:
            if curr_health == 'scraping id banned':
                print('banned id-----', scraping_id)
                driver.quit()
                health_vars['consecutive_fail_ct'] = 0
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

        
        print(user_name, user_id)

        wait_time = random.randrange(2, 5)
        sleep(wait_time)

        driver.get("https://www.instagram.com/{user_name}/".format(user_name=user_name))

        wait_time = random.randrange(2, 5)
        sleep(wait_time)
        
        ###################### checking account ######################
        if not check_handle_valid(driver):
            failed_scrape_list.append(user_name)
            health_vars['consecutive_fail_ct'] += 1
            user_name_status.update({user_name:{'status': 'failed', 'reason': 'user name changed'}})
            return_status_resp({user_name:user_name_status[user_name]})
            print('skipping further process------')
            continue
        else:
            health_vars['consecutive_fail_ct'] = 0

        ###################### scrape user info ######################
        user_pvt = user_handle_pvt(driver)
        try:
            user_df, post_count = get_user_details(driver, user_name, user_id, user_pvt)
            user_data_to_api(user_df)
            user_df.to_excel(user_name + "_details.xlsx", encoding='utf-8', index=False)
        except Exception as e:
            print(e)
            pass

        if user_pvt:
            user_name_status.update({user_name: {'status': 'scraped', 'reason': 'private account'}})
            return_status_resp({user_name:user_name_status[user_name]})
            print('skipping further process------')
            continue

        if post_count == 0:
            print('no post-----')
            continue
        
        ###################### processing reels ######################
        process_reel(driver, user_name, user_id, user_name_status, health_vars)
        ###################### processing posts ######################
        process_posts(driver, user_name, user_id, user_name_status, health_vars)
        
    scraping_id_status['status'] = 'free'
    return_status_resp(user_name_status, scraping_id_status)
    return 'batch scraping completed----'