from time import sleep
from data.one_time_insta_login import do_insta_login
import random
import traceback
from utils.exist_check import check_handle_valid, user_handle_pvt, login_maintained_check
from utils.read_from_html import get_user_details
from constants import CONSECUTIVE_FAIL_LIMIT, SELENIUM_FAIL_LIMIT, CRED_AVAILABLE, USER_NAME, PASSWORD, CHROMEDRIVER, HEADLESS, REUSE_SESSION, BATCH_SIZE
from data.send_data_to_apis import request_scraping_creds, fail_status_api, user_data_to_api, get_user_name_batch, update_scrape_id_status
from utils.selenium_driver import get_web_driver
from utils.exist_check import check_if_logged_in
from data.scrape_reels import process_reel
from data.scrape_posts import process_posts


def health_good(health_vars):
    if health_vars['page_not_avail'] >= CONSECUTIVE_FAIL_LIMIT:
        print('scraping id banned-------')
        return False
    return True


def retry_login(driver):
    driver.close()
    print('maybe id banned, retrying login ------')
    try:
        update_scrape_id_status(scraping_id, 'banned')
        scraping_id, password = request_scraping_creds()
        login_success, driver = do_insta_login(scraping_id, password)

        if not login_success:
            print('login failed, exiting------')
            return None
        return driver
    except Exception:
        traceback.print_exc()
        print('failure in re-login process, POS:pb-2 ------')
    return None

def health_check_process(health_vars):
    pass




def start_batch_processing(batch=None):
    

    ###################### session usage ######################
    scraping_id, password = USER_NAME, PASSWORD
    if REUSE_SESSION:
        driver = get_web_driver(CHROMEDRIVER, HEADLESS)
        login_success = check_if_logged_in(driver)
    else:
        login_success, driver = do_insta_login(scraping_id, password)

    if not login_success:
        driver.close()
        login_success, driver = do_insta_login(scraping_id, password)
    
    if not login_success:
        driver.close()
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
    
    ###################### health variables ######################
    health_vars = {'page_not_avail':0, 'selenium_fail':0}


    ###################### batch processing starts ######################
    curr_num = 1
    for user_name, user_id in batch.items():
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
            if not login_maintained_check(driver) and not health_good(health_vars):

                driver = retry_login(driver)
                if not driver:  return
            
            ###################### checking account ######################
            if not check_handle_valid(driver):
                user_data_dict["scrape_status"] = 'failure'
                user_data_dict["reason"] = []
                user_data_dict["reason"].append('page_not_available')
                fail_status_api(user_data_dict)
                print('skipping further process------')
                health_vars['page_not_avail'] += 1
                continue
            else:
                health_vars['page_not_avail'] = 0

            ###################### scrape user info ######################
            user_pvt = user_handle_pvt(driver)
            try:
                user_df, post_count = get_user_details(driver, user_name, user_id, user_pvt)
                user_data_to_api(user_df)
                user_df.to_excel(user_name + "_details.xlsx", encoding='utf-8', index=False)
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
            # process_posts(driver, user_name, user_id)

        except Exception:
            traceback.print_exc()
            user_data_dict["scrape_status"] = 'failure'
            user_data_dict["reason"] = []
            user_data_dict["reason"].append('selenium_failed')
            print(f'no details scraped for {user_name}, maybe a major process like details, reel or post scrape failed, POS:pb-1 ------')
            fail_status_api(user_data_dict)
    print('batch scraping completed----')
    return