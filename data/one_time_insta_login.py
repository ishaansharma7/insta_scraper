import os
from time import sleep
import traceback
from utils.selenium_driver import get_web_driver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import shutil
from flask import current_app
from constants import CHROMEDRIVER, HEADLESS
import random


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def automated_login(driver, username, password):
    print('started')

    sleep(random.randrange(2, 7))

    username_field = driver.find_element_by_name("username")
    password_filed = driver.find_element_by_name("password")

    username_field.send_keys(username)
    password_filed.send_keys(password)
    print('creds entered')

    log_in_page = driver.find_element_by_xpath("""//*[@id="loginForm"]/div/div[3]/button/div""")
    ActionChains(driver).move_to_element(log_in_page).pause(1).click(log_in_page).perform()

    body = driver.find_element_by_tag_name("body")
    wait = WebDriverWait(driver, 10, poll_frequency=0.5)
    wait.until(EC.staleness_of(body))
    print(driver.current_url)

    not_now_exists = check_exists_by_xpath(driver, """//*[@id="react-root"]/section/main/div/div/div/div/button""")
    if not_now_exists:
        not_now = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/div/div/div/button""")
        ActionChains(driver).move_to_element(not_now).pause(1).click(not_now).perform()

    not_now_alternate = check_exists_by_xpath(driver, """//*[@id="mount_0_0_3s"]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]""")
    if not_now_alternate:
        not_now = driver.find_element_by_xpath("""//*[@id="mount_0_0_3s"]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]""")
        ActionChains(driver).move_to_element(not_now).pause(1).click(not_now).perform()
    
    not_now_alternate2 = check_exists_by_xpath(driver, """//*[@id="mount_0_0_WZ"]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/button""")
    if not_now_alternate2:
        not_now = driver.find_element_by_xpath("""//*[@id="mount_0_0_WZ"]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/button""")
        ActionChains(driver).move_to_element(not_now).pause(1).click(not_now).perform()
    
    not_now_alternate3 = check_exists_by_xpath(driver, """//*[@id="mount_0_0_IB"]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div/div/button""")
    if not_now_alternate3:
        not_now = driver.find_element_by_xpath("""//*[@id="mount_0_0_IB"]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div/div/button""")
        ActionChains(driver).move_to_element(not_now).pause(1).click(not_now).perform()

    print(driver.current_url)
    wait_time = random.randrange(2, 7)
    sleep(wait_time)

    notif_exists = check_exists_by_xpath(driver, """/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]""")
    if notif_exists:
        ok =  driver.find_element_by_xpath("""/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]""")
        ActionChains(driver).move_to_element(ok).pause(1).click(ok).perform()
    print('login done')


def do_insta_login(USER_NAME, PASSWORD):
    try:
        session_path = os.path.join(os.getcwd(), 'selenium_session')
        if os.path.exists(session_path):
            print('Previous session found------')
            print('removing previous session------')
            shutil.rmtree(session_path)
        driver = get_web_driver(CHROMEDRIVER, HEADLESS)
        url = "https://www.instagram.com/"
        driver.get(url)
        automated_login(driver, USER_NAME, PASSWORD)
        sleep(2)
        return True, driver
    except Exception:
        traceback.print_exc()
        return False, None


if __name__ == '__main__':
    do_insta_login()