from time import sleep
import traceback
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_high_data(driver):
    driver.get('https://www.instagram.com/harshit.tewatia/')
    sleep(10)
    failed = False
    try:
        ul = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, '_acaz')))
        print([ele.text for ele in ul])
        # do logic here
    except Exception:
        traceback.print_exc()
        print('failed to scrape highlights-----')
        print('retrying-----')
        failed = True
    if failed:
        try:
            sleep(5)
            ul = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, '_acaz')))
            print([ele.text for ele in ul])
        # do logic here
        except Exception:
            traceback.print_exc()
            print('unable to scrape highlights-----')
            print('skipping highlights-----')