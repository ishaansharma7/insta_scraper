from data.one_time_insta_login import do_insta_login
from constants import USER_NAME, PASSWORD, CHROMEDRIVER, HEADLESS, REUSE_SESSION
from data.send_data_to_apis import request_scraping_creds
from utils.selenium_driver import get_web_driver
from utils.exist_check import check_if_logged_in


def get_session():
    scraping_id, password = USER_NAME, PASSWORD
    if REUSE_SESSION:
        driver = get_web_driver(CHROMEDRIVER, HEADLESS)
        login_success = check_if_logged_in(driver)
    else:
        login_success, driver = do_insta_login(scraping_id, password)

    if not login_success:
        if driver: driver.close()
        login_success, driver = do_insta_login(scraping_id, password)
    
    if not login_success:
        if driver: driver.close()
        print('login failed, retrying------')
        scraping_id, password = request_scraping_creds()
        login_success, driver = do_insta_login(scraping_id, password)
    return login_success, driver