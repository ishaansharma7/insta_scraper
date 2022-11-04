import pandas as pd
from time import sleep
import random
from utils.read_from_html import get_reel_details
from data.send_data_to_apis import reels_data_to_api, return_status_resp

def process_reel(driver, user_name, user_id, user_name_status, health_vars):
    ###################### pd dataframe ######################
    media_df = pd.DataFrame(columns=["user_name", "media_url", "shortcode", "comments_count", "like_count", "view_count", "user_id"])
    
    ###################### scraping reels data ######################
    driver.get("https://www.instagram.com/{user_name}/reels/".format(user_name=user_name))
    wait_time = random.randrange(5, 7)
    SCROLL_PAUSE_TIME = wait_time
    count = 0
    while count <= 5:
        media_df, sele_worked = get_reel_details(driver.page_source, user_name, user_id, media_df)
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
        count += 1
    
    if len(media_df) == 0 and not sele_worked:
        health_vars['selenium_fail_ct'] += 1
        print('no details scraped------')
        return
    else:
        health_vars['selenium_fail_ct'] = 0
        print(f'{user_name} scraped------')
        if len(media_df) == 0:
            user_name_status.update({user_name: {'status': 'scraped', 'reason': 'no reels uploaded'}})
        else:
            user_name_status.update({user_name: {'status': 'scraped', 'reason': 'successful'}})
    
    reels_data_to_api(media_df)
    return_status_resp({user_name:user_name_status[user_name]})
    # media_df.to_excel(user_name + "_media.xlsx", encoding='utf-8', index=False)
    wait_time = random.randrange(3, 7)
    sleep(wait_time)
