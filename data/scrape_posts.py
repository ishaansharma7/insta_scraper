import pandas as pd
from time import sleep
import random
from utils.read_from_html import get_post_details, get_shortcodes_reels, get_full_reel_details, per_hover
from data.send_data_to_apis import reels_data_to_api, post_data_to_api

def process_posts(driver, user_name, user_id, user_name_status, health_vars):
    print('scraping post data-----')
    ###################### pd dataframe ######################
    # media_df = pd.DataFrame(columns=["user_name", "media_url", "shortcode", "comments_count", "like_count", "view_count", "user_id", "alt_text"])
    ###################### scraping posts data ######################
    driver.get("https://www.instagram.com/{user_name}/".format(user_name=user_name))
    wait_time = random.randrange(2, 5)
    SCROLL_PAUSE_TIME = wait_time
    count = 0
    covered_shortcodes = {}
    ct_dict = {'ct':0}
    scraped_post_list = []
    while count <= 2:
        # media_df, sele_worked = get_post_details(driver.page_source, user_name, user_id, covered_shortcodes, media_df)
        local_list = per_hover(driver, covered_shortcodes, ct_dict, user_name, user_id)
        scraped_post_list.extend(local_list)
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
    print('no. of scrapped post-----', ct_dict['ct'])
    post_data_to_api(scraped_post_list)
    # if len(media_df) == 0 and not sele_worked:
    #     print('no details scraped------')
    #     return
    # else:
    #     print(f'{user_name} scraped------')
        
    # posts_data_to_api(media_df)
    # media_df.to_excel(user_name + '_post'+ "_media.xlsx", encoding='utf-8', index=False)
    wait_time = random.randrange(3, 7)
    sleep(wait_time)
