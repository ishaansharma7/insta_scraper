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


def check_handle_valid2(driver):
    valid_handle = True
    try:
        page_not_avail =  WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0_CF"]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div')))
        valid_handle = False
        print('not a valid user handle!!!--------')
    except Exception:
        traceback.print_exc()
        print('valid user handle--------')
    return valid_handle