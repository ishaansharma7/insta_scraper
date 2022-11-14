import pandas as pd
from time import sleep
import random
from utils.read_from_html import get_reel_details, get_shortcodes_reels, get_full_reel_details
from data.send_data_to_apis import reels_data_to_api, reel_status_api, fail_status_api
import traceback

def process_reel(driver, user_name, user_id):
    ###################### variables ######################
    media_df = pd.DataFrame(columns=["user_name", "media_url", "shortcode", "comments_count", "like_count", "view_count", "user_id"])
    user_data_dict = {
        'user_name': user_name,
        'user_id': user_id,
        'scrape_status': 'not_scraped',
        'reason': []
    }

    try:
        ###################### scraping reels data ######################
        driver.get("https://www.instagram.com/{user_name}/reels/".format(user_name=user_name))
        sleep(5)
        wait_time = random.randrange(2, 5)
        SCROLL_PAUSE_TIME = wait_time
        shortcode_set = []
        count = 0
        while count <= 5:
            media_df, sele_worked = get_reel_details(driver.page_source, user_name, user_id, media_df)
            local_set = get_shortcodes_reels(driver)
            shortcode_set.extend(local_set)
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

        media_df_len = len(media_df)
        if media_df_len == 0 and not sele_worked:
            user_data_dict["scrape_status"] = 'failure'
            user_data_dict["reason"] = []
            user_data_dict["reason"].append('selenium_failed')
            print(f'no details scraped for {user_name}, maybe a failure in reels scraping, POS:sr-2 ------')
            # stop the code here and send failure status
            fail_status_api(user_data_dict)
            return
        else:
            print(f'{user_name} scraped, scraped reel count: {media_df_len} ------')
            if media_df_len == 0:
                user_data_dict["scrape_status"] = 'scraped'
                user_data_dict["reason"].append('no_reels_uploaded')
            else:
                user_data_dict["scrape_status"] = 'scraped'
                user_data_dict["reason"].append('successful')
                reels_data_to_api(media_df)
                get_full_reel_details(driver, shortcode_set)

        media_df.to_excel(user_name + "_media.xlsx", encoding='utf-8', index=False)
        wait_time = random.randrange(3, 7)
        reel_status_api(user_data_dict)
        sleep(wait_time)
    except Exception:
        traceback.print_exc()
        user_data_dict["scrape_status"] = 'failure'
        user_data_dict["reason"] = []
        user_data_dict["reason"].append('selenium_failed')
        print(f'no details scraped for {user_name}, maybe a failure in reels scraping, POS:sr-3 ------')
        fail_status_api(user_data_dict)