import os
from dotenv import load_dotenv

load_dotenv()

CHROMEDRIVER = os.environ['CHROMEDRIVER']
HEADLESS = True if os.environ['HEADLESS'] == '1' else False
CRED_AVAILABLE = True if os.environ['CRED_AVAILABLE'] == '1' else False
REUSE_SESSION = True if os.environ['REUSE_SESSION'] == '1' else False
USER_NAME = os.environ['USER_NAME']
PASSWORD = os.environ['PASSWORD']
CONSECUTIVE_FAIL_LIMIT = int(os.environ['CONSECUTIVE_FAIL_LIMIT'])
SELENIUM_FAIL_LIMIT = int(os.environ['SELENIUM_FAIL_LIMIT'])


BATCH_SIZE = int(os.environ['BATCH_SIZE'])

API_BASE_URL=os.environ['API_BASE_URL']
SEND_USERNAME_URL= API_BASE_URL + '/v1/instagram/manager/send/user-names/'
UPDATE_SCRAPEID_STATUS_URL = API_BASE_URL + '/v1/instagram/manager/update/status/scrape-id/'
SEND_SCRAPEID_URL = API_BASE_URL + '/v1/instagram/manager/send/scrape-id/'
REELS_DATA_URL = API_BASE_URL + '/v1/instagram/manager/update/reels-data/'
USER_DATA_URL = API_BASE_URL + '/v1/instagram/manager/update/user-data/'
USER_NAME_STATUS_URL = API_BASE_URL + '/v1/instagram/manager/update/status/user-name/'

insta_url = os.environ["INSTA_GRAPH_URL"]
mymoney_insta_id = os.environ["MYMONEY_INSTA_ID"]
access_token = os.environ["INSTA_ACCESS_TOKEN"]

#instagram DB details
SQL_HOST = os.environ["SQL_HOST"]
PSQL_PORT = os.environ["PSQL_PORT"]
SQL_DATABASE = os.environ["SQL_DATABASE"]
SQL_USER_NAME = os.environ["SQL_USER_NAME"]
SQL_PASSWORD = os.environ["SQL_PASSWORD"]

#rewards DB details
REWARDS_IP = os.environ["REWARDS_IP"]
REWARDS_PASS = os.environ["REWARDS_PASS"]
REWARDS_DB = os.environ["REWARDS_DB"]
REWARDS_USER = os.environ["REWARDS_USER"]