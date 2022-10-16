import requests
import json
import traceback
from constants import UPDATE_SCRAPEID_STATUS_URL, SEND_SCRAPEID_URL


def update_scrape_id_status(scraping_id='', status=''):
    try:
        url = UPDATE_SCRAPEID_STATUS_URL
        payload = json.dumps({
        "scrape_id": scraping_id,
        "status": status
        })
        headers = {
        'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception:
        traceback.print_exc()

def request_scraping_creds(first_time=True, scraping_id='', status=''):
    if not first_time:
        update_scrape_id_status(scraping_id, status)
    try:
        url = SEND_SCRAPEID_URL
        payload={}
        response = requests.request("GET", url, data=payload).json()
        scraping_id = response['data']['result']['scrape_id']
        password = response['data']['result']['password']
        return scraping_id, password
    except Exception:
        traceback.print_exc()
        return None, None


def return_resp(user_name_status: dict, scraping_id_status: dict):
    try:
        f_resp = {'user_name_status': [],}
        for k, v in user_name_status.items():
            v['user_name'] = k
            f_resp['user_name_status'].append(v)
        print(f_resp)
        update_scrape_id_status(scraping_id_status['scrape_id'], scraping_id_status['status'])
    except Exception:
        traceback.print_exc()
    return
    