import os
from dotenv import load_dotenv

load_dotenv()

CHROMEDRIVER = os.environ['CHROMEDRIVER']
HEADLESS = True if os.environ['HEADLESS'] == '1' else False
CONSECUTIVE_FAIL_LIMIT = int(os.environ['CONSECUTIVE_FAIL_LIMIT'])
SELENIUM_FAIL_LIMIT = int(os.environ['SELENIUM_FAIL_LIMIT'])


API_BASE_URL=os.environ['API_BASE_URL']
SEND_USERNAME_URL= API_BASE_URL + '/manager/send/user-names/'
UPDATE_SCRAPEID_STATUS_URL = API_BASE_URL + '/manager/update/status/scrape-id/'
SEND_SCRAPEID_URL = API_BASE_URL + '/manager/send/scrape-id/'