from data.send_data_to_apis import get_shortcode_using_username
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from data.send_data_to_apis import update_new_user_name
from bs4 import BeautifulSoup
from time import sleep
import traceback
from utils.exist_check import check_handle_valid


def find_new_user_name(driver, user_name):
    new_user_name = None
    try:
        shortcode = get_shortcode_using_username(user_name)
        if not shortcode:   return None
        url = f'https://www.instagram.com/p/{shortcode}/'
        driver.get(url)
        sleep(5)
        beautifulSoupText = BeautifulSoup(driver.page_source, 'html.parser')
        spans = beautifulSoupText.find_all("span", attrs={"class":"_aap6 _aap7 _aap8"})
        for span in spans:
            new_user_name = span.text
            break
        print('new_user_name:', new_user_name)
        return new_user_name
    except Exception:
        traceback.print_exc()
        print('unable to find new user_name -----')
    return new_user_name


def process_invalid_username(driver, old_user_name):
    try:
        new_user_name = find_new_user_name(driver, old_user_name)
        if not new_user_name: return None, None
        if new_user_name == old_user_name:
            print('old and new username same -----')
            return None, None
        driver.get("https://www.instagram.com/{user_name}/".format(user_name=new_user_name))
        if not check_handle_valid(driver):
            print('again username not valid -----')
            return None, None
        # update new_username in media table using api
        update_new_user_name(new_user_name, old_user_name)
        return True, new_user_name 
    except Exception:
        traceback.print_exc()
    return None, None
