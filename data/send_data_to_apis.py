from pprint import pprint
import requests
import json
import traceback
from constants import UPDATE_SCRAPEID_STATUS_URL, SEND_SCRAPEID_URL, REELS_DATA_URL, USER_DATA_URL, SEND_USERNAME_URL, USER_NAME_STATUS_URL
from datetime import datetime


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

def reels_data_to_api(media_df):
    print('sending reels data-----')
    reel_list = []
    for index, row in media_df.iterrows():
        comments_count_int = number_clean_up(row["comments_count"])
        like_count_int = number_clean_up(row["like_count"])
        view_count_int = number_clean_up(row["view_count"])
        c_row = {
            'user_name': row["user_name"],
            'media_url': row["media_url"],
            'shortcode': row["shortcode"],
            'comments_count': row["comments_count"],
			'like_count': row["like_count"],
            'view_count': row["view_count"],
            'user_id': row["user_id"],
            'last_updated': str(datetime.now().date()),
            'like_count_int': like_count_int,
            'comments_count_int': comments_count_int,
            'view_count_int': view_count_int,
            'permalink': 'https://www.instagram.com/p/' + row["shortcode"]
        }
        reel_list.append(c_row)
    try:
        url = REELS_DATA_URL
        payload = json.dumps({
        "reels_data": reel_list,
        })
        headers = {
        'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception:
        traceback.print_exc()

    
def user_data_to_api(user_df):
    user_list = []
    for index, row in user_df.iterrows():
        followers_count_int = number_clean_up(row["followers_count"])
        following_count_int = number_clean_up(row["following_count"])
        post_count_int = number_clean_up(row["post_count"])
        c_row = {
            'insta_user_name':row["insta_user_name"],
            'profile_url':row["profile_url"],
            'user_name':row["user_name"],
            'bio':row["bio"],
            'post_count':row["post_count"],
            'followers_count':row["followers_count"],
            'following_count': row["following_count"],
            'account_type':row["account_type"],
			'followers_count_int':followers_count_int,
            'following_count_int':following_count_int,
            'post_count_int':post_count_int,
            'last_updated':str(datetime.now().date()),
            'highlights':row["highlights"]
        }
        user_list.append(c_row)
    try:
        url = USER_DATA_URL
        payload = json.dumps({
        "user_data": user_list,
        })
        headers = {
        'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception:
        traceback.print_exc()

def number_clean_up(clean_value):
	try:
		if not isinstance(clean_value, int):
			# import pdb; pdb.set_trace()
			clean_value = clean_value.replace(",", "")
			clean_value = clean_value.replace(".", "")
			if "k" in clean_value.lower():
				clean_value = clean_value.replace("K", "")
				clean_value = int(clean_value) * 1000
			elif "m" in clean_value.lower():
				clean_value = clean_value.replace("M", "")
				clean_value = int(clean_value) * 1000000
	except Exception as e:
		traceback.print_exc()
		print(clean_value)
		pass
	return clean_value

def return_status_resp(user_name_status: dict, scraping_id_status: dict=None):
    try:
        user_name_list = []
        for k, v in user_name_status.items():
            if 'resp_send' in v: continue
            v['user_name'] = k
            v['resp_send'] = True
            user_name_list.append(v)

        if scraping_id_status:
            update_scrape_id_status(scraping_id_status['scrape_id'], scraping_id_status['status'])
        
        if not len(user_name_list): return
        url = USER_NAME_STATUS_URL
        payload = json.dumps({
        "user_name_status": user_name_list,
        })
        headers = {
        'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print('user_name_list-------')
        pprint(user_name_list)

    except Exception:
        traceback.print_exc()
    return
    
def get_user_name_batch(limit=5):
    try:
        batch = requests.get(SEND_USERNAME_URL, params={'limit':limit}).json()['data']['result']
        return batch
    except Exception:
        traceback.print_exc()
    return None