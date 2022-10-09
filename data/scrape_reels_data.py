import os
import traceback
from utils.read_from_html import get_reel_details, get_user_details
from dotenv import load_dotenv
from utils.selenium_driver import get_web_driver
from utils.exist_check import check_if_logged_in, check_handle_valid
import pandas as pd
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import random

load_dotenv()
CHROMEDRIVER = os.getenv('CHROMEDRIVER')
HEADLESS = True if os.getenv('HEADLESS') == '1' else False

def get_users_reel_data(user_dict, driver):
    for user_id, user_name,  in user_dict.items():
        media_df = pd.DataFrame(columns=["user_name", "media_url", "shortcode", "comments_count", "like_count", "view_count", "user_id"])

        print(user_name, user_id)

        wait_time = random.randrange(3, 7)
        sleep(wait_time)

        driver.get("https://www.instagram.com/{user_name}/reels/".format(user_name=user_name))

        
        wait_time = random.randrange(3, 5)
        sleep(wait_time)
        
        if not check_handle_valid(driver):
            print('skipping further process------')
            continue

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
        
        media_df.to_excel(user_name + "_media.xlsx", encoding='utf-8', index=False)
        # if user_df:
        #     user_df.to_excel(user_name + "_details.xlsx", encoding='utf-8', index=False)
        wait_time = random.randrange(3, 7)
        sleep(wait_time)


if __name__ == '__main__':
    driver = get_web_driver(CHROMEDRIVER, HEADLESS)
    driver.maximize_window()
    # if not check_if_logged_in(driver):
    #     print('Aborting further process!!!--------')
    #     driver.quit()
    #     exit()
    user_dict = {
        "ffb2be61c7544dbd9bdbddd6abd37e87" : "sumisunildas23",
        "ffb2be61c7544dbd9bdbddd6abd37e88" : "shri_radheradhe",
    }
    get_users_reel_data(user_dict, driver)
    driver.quit()