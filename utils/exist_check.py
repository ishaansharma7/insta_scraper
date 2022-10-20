from time import sleep, time
import traceback
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def check_if_logged_in(driver):
    driver.get('https://www.instagram.com/')
    logged_in = False
    try:
        home_dm_profile_bar =  WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, '_acut')))
        logged_in = True
        print('login session present--------')
    except Exception:
        traceback.print_exc()
        print('No login session present!!!--------')
    return logged_in


def check_handle_valid(driver):
    valid_handle = True
    try:
        # sleep(20)
        page_not_avail = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'h2')))
        if "Sorry, this page isn't available." in page_not_avail[0].text:
            valid_handle = False
    except Exception:
        pass
    if valid_handle:
        print('valid user handle--------')
    else:
        print('not a valid user handle!!!--------')
    return valid_handle


def check_if_logged_in(driver):
    driver.get('https://www.instagram.com/')
    logged_in = False
    try:
        username_field =  WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.NAME, 'username')))
        print('No login session present!!!--------')
    except Exception:
        logged_in = True
        print('login session present--------')
    return logged_in


def user_handle_pvt(driver):
    try:
        private_ele =  WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME, '_aa_u')))
        print('private user handle--------')
        return True
    except Exception:
        return False