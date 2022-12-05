from pprint import pprint
import requests
import json
import traceback
from constants import (UPDATE_SCRAPEID_STATUS_URL, SEND_SCRAPEID_URL, REELS_DATA_URL,
USER_DATA_URL, SEND_USERNAME_URL, USER_NAME_STATUS_URL, POSTS_DATA_URL, SINGLE_REEL_URL,
SCROLL_POSTS_URL, SCRAPE_STATUS_URL, FAILURE_STATUS_URL, POPU_REELS_DATE_URL, UPDATE_NEW_USERNAME_URL,
GET_SHORTCODE_USERNAME
)
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
			# clean_value = clean_value.replace(".", "")
			if "k" in clean_value.lower():
				clean_value = clean_value.replace("K", "")
				clean_value = float(clean_value) * 1000
			elif "m" in clean_value.lower():
				clean_value = clean_value.replace("M", "")
				clean_value = float(clean_value) * 1000000
	except Exception as e:
		traceback.print_exc()
		print(clean_value)
		pass
	return clean_value

def reel_status_api(user_data_dict: dict, scraping_id_status: dict=None):
    try:
        if scraping_id_status:
            print('scraping_id_status send-----')
            update_scrape_id_status(scraping_id_status['scrape_id'], scraping_id_status['status'])
        
        url = SCRAPE_STATUS_URL
        user_data_dict['last_updated'] = str(datetime.now().date())
        payload = json.dumps({
        "reel_scrape_status": user_data_dict,
        })
        headers = {
        'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception:
        traceback.print_exc()
        print('unable to send reel status, POS:sdta-1 -----')
    return

def fail_status_api(user_data_dict: dict):
    try:
        
        url = FAILURE_STATUS_URL
        user_data_dict['last_updated'] = str(datetime.now().date())
        payload = json.dumps({
        "fail_status": user_data_dict,
        })
        headers = {
        'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception:
        traceback.print_exc()
        print('unable to send reel status, POS:sdta-1 -----')
    return
    
def get_user_name_batch(limit=5):
    try:
        batch = requests.get(SEND_USERNAME_URL, params={'limit':limit}).json()['data']['result']
        return batch
    except Exception:
        traceback.print_exc()
    return None

def posts_data_to_api(media_df):
    print('sending posts data-----')
    post_list = []
    for index, row in media_df.iterrows():
        c_row = {
            'user_name': row["user_name"],
            'media_url': row["media_url"],
            'shortcode': row["shortcode"],
            'comments_count': row["comments_count"],
			'like_count': row["like_count"],
            'view_count': row["view_count"],
            'user_id': row["user_id"],
            'alt_text': row["alt_text"],
            'last_updated': str(datetime.now().date())
        }
        post_list.append(c_row)
    try:
        url = POSTS_DATA_URL
        payload = json.dumps({
        "posts_data": post_list,
        })
        headers = {
        'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception:
        traceback.print_exc()


def single_reel_data_to_api(reel_dict):
    print('sending single reel data -----')
    
    try:
        url = SINGLE_REEL_URL
        payload = json.dumps({
        "reel_data": reel_dict,
        })
        headers = {
        'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception:
        traceback.print_exc()

def post_data_to_api(scraped_post_list):
    print('sending posts data to api -----')
    for row in scraped_post_list:
        row['comments_count_int'] = number_clean_up(row["comments_count"])
        row['like_count_int'] = number_clean_up(row["like_count"])
        row['last_updated'] = str(datetime.now().date())
        row['permalink'] = 'https://www.instagram.com/p/' + row["shortcode"]
    try:
        url = SCROLL_POSTS_URL
        payload = json.dumps({
        "posts_data": scraped_post_list,
        })
        headers = {
        'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception:
        traceback.print_exc()

def populate_reels_date(date_dict):
    print('reel date population api -----')
    try:
        url = POPU_REELS_DATE_URL
        payload = json.dumps({
        "reels_dict": date_dict,
        })
        headers = {
        'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception:
        traceback.print_exc()
    return None


def get_shortcode_using_username(user_name):
    print('get shortcode api -----')
    try:
        url = GET_SHORTCODE_USERNAME
        payload = json.dumps({
        "user_name": user_name
        })
        headers = {
        'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        data_dict = response.json()
        return data_dict['data']['result']['shortcode']
    except Exception:
        traceback.print_exc()
    return None

def update_new_user_name(new_user_name, old_user_name):
    print('new user_name update api-----')
    try:
        url = UPDATE_NEW_USERNAME_URL
        payload = json.dumps({
        "new_user_name": new_user_name,
        "old_user_name": old_user_name
        })
        headers = {
        'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception:
        traceback.print_exc()