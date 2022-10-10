import os
from dotenv import load_dotenv

load_dotenv()

CHROMEDRIVER = os.environ['CHROMEDRIVER']
HEADLESS = True if os.environ['HEADLESS'] == '1' else False
CONSECUTIVE_FAIL_LIMIT = int(os.environ['CONSECUTIVE_FAIL_LIMIT'])
SELENIUM_FAIL_LIMIT = int(os.environ['SELENIUM_FAIL_LIMIT'])