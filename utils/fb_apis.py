import traceback
import requests
import psycopg2.extras
from time  import sleep
from utils.insta_db import insert_media_details_to_db, insert_user_detail_into_db, update_insta_user_fb_response_status
from utils.mymoney_db import update_rewards_user_profile_status

from constants import insta_url, mymoney_insta_id, access_token


def get_user_details_from_api(user):
    user_name = user.get("acc_name", None)
    if user_name:
        print("\nfetching details for user:", user_name)
        
        fields = "business_discovery.username(%s){followers_count,media_count,biography,username,website,name,follows_count,ig_id,id,profile_picture_url,media.limit(100){media_type,owner,caption,comments_count,id,like_count,media_product_type,media_url,permalink,timestamp,username,video_title}}"%(user_name)
        url = "{insta_url}{user_id}?fields={fields}&access_token={access_token}".format(insta_url=insta_url, user_id=mymoney_insta_id, fields=fields, access_token=access_token)
        response = requests.get(url)
        res_json = response.json()

        if "business_discovery" in res_json:
            res_json = res_json["business_discovery"]
            return res_json
        else:
            print(res_json)
            update_rewards_user_profile_status(user_name)
            update_insta_user_fb_response_status(user_name)
            return None


def get_details_from_response(user, api_response):
    insert_user_detail_into_db(user, api_response)
    if "media" in api_response:
        media_list = api_response["media"].get("data",[])
        print(len(media_list))
        if media_list:
            print(len(media_list))
            for item in media_list:
                insert_media_details_to_db(item, None)
