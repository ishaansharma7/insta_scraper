from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def get_web_driver(CHROMEDRIVER, headless=False):
    PROJECT_ROOT = os.getcwd()
    DRIVER_BIN = os.path.join(PROJECT_ROOT, CHROMEDRIVER)
    print(DRIVER_BIN)
    opt = Options()
    if headless:
        opt.headless = True
        opt.add_argument('--no-sandbox')
        opt.add_argument('--disable-dev-shm-usage')
        opt.add_argument('--disable-gpu')
        opt.add_argument("--window-size=1024,768")
    opt.add_argument("user-data-dir=selenium_session")
    driver = webdriver.Chrome(executable_path=DRIVER_BIN, options=opt)
    if not headless:
        driver.maximize_window()
    return driver