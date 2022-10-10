from time import sleep
from data.one_time_insta_login import do_insta_login
from flask import current_app
import pandas as pd
import random
from utils.exist_check import check_handle_valid
from utils.read_from_html import get_reel_details, get_user_details
from constants import CONSECUTIVE_FAIL_LIMIT, SELENIUM_FAIL_LIMIT

def request_scrapping_creds():
    USER_NAME = current_app.config['USER_NAME']
    PASSWORD = current_app.config['PASSWORD']
    return USER_NAME, PASSWORD

def health_check(consecutive_fail_ct, selenium_fail_ct):
    if consecutive_fail_ct >= CONSECUTIVE_FAIL_LIMIT:
        return 'scrapping id banned'
    if selenium_fail_ct >= SELENIUM_FAIL_LIMIT:
        return 'selenium code break'
    return None


def process_reels(batch: dict):

    scraping_id, password = request_scrapping_creds()
    login_success, driver = do_insta_login(scraping_id, password)
    if not login_success:
        print('login failed exiting------')
        return
        # handle this case

    # 0 means data not processed
    # 1 means data processed
    # 2 means user_name changed
    user_name_status = {v: 0 for k, v in batch.items()}
    failed_scrape_list = []
    consecutive_fail_ct = 0     # help to identify scraping ID banned or not
    selenium_fail_ct = 0        # help to identify selenium code break

    for user_id, user_name,  in batch.items():


        media_df = pd.DataFrame(columns=["user_name", "media_url", "shortcode", "comments_count", "like_count", "view_count", "user_id"])
        print(user_name, user_id)

        wait_time = random.randrange(3, 7)
        sleep(wait_time)

        driver.get("https://www.instagram.com/{user_name}/reels/".format(user_name=user_name))

        
        wait_time = random.randrange(3, 5)
        sleep(wait_time)
        
        if not check_handle_valid(driver):
            failed_scrape_list.append(user_name)
            consecutive_fail_ct += 1
            print('skipping further process------')
            continue
        else:
            consecutive_fail_ct = 0
            user_name_status.update(**{k: 2 for k in failed_scrape_list})
            failed_scrape_list.clear()


        user_df = get_user_details(driver.page_source, user_name, user_id)


        wait_time = random.randrange(2, 6)
        SCROLL_PAUSE_TIME = wait_time
        while True:
            last_height = driver.execute_script("return document.body.scrollHeight")

            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            media_df = get_reel_details(driver.page_source, user_name, user_id, media_df)
        
        if not len(media_df):
            selenium_fail_ct += 1
            print('no details scrapped------')
            continue
        else:
            selenium_fail_ct = 0
            print(f'{user_name} scrapped------')

        # here add the db code
        # media_df.to_excel(user_name + "_media.xlsx", encoding='utf-8', index=False)
        # if user_df:
        #     user_df.to_excel(user_name + "_details.xlsx", encoding='utf-8', index=False)
        wait_time = random.randrange(3, 7)
        sleep(wait_time)
    
    return {'scrape_status': user_name_status, 'scraping_id': scraping_id}