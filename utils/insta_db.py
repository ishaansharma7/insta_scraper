import re
import json
import traceback
from datetime import datetime
import psycopg2.extras
from utils.db_utils import get_insta_db_connection
from utils.mymoney_db import update_last_update_time_social_account


hashtag_regex = "#(\w+)"
mentions_regex = "@(\w+)"


def insert_media_details_to_db(media, existing_user_id):
    try:
        cursor = get_insta_db_connection().cursor()
        user_id = existing_user_id if existing_user_id else media.get("owner").get("id", "")
        hashtag_list = re.findall(hashtag_regex, media.get("caption",""))
        mentions_list = re.findall(mentions_regex, media.get("caption",""))
        permalink = media.get("permalink", "")
        shortcode = None
        if permalink:
            shortcode = permalink.split("/")[4]
        insert_query = '''INSERT INTO public.media (id, username, media_url, thumbnail_url, media_product_type, media_type,
                        permalink, caption, video_title, shortcode, media_date, user_id, comments_count, like_count, hastags, mentions, last_updated)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                        ON CONFLICT (shortcode) DO UPDATE SET comments_count = %s, 
                        like_count = %s, media_url = %s, user_id = %s, thumbnail_url = %s, username=%s, last_updated=%s'''
        values = (media.get("id", ""), media.get("username", ""), media.get("media_url", None), media.get("thumbnail_url", None), 
                    media.get("media_product_type", None),media.get("media_type", None), permalink, media.get("caption", ""), 
                    media.get("video_title", None), shortcode, media.get("timestamp", ""), user_id, media.get("comments_count", None), 
                    media.get("like_count", None), json.dumps(hashtag_list), json.dumps(mentions_list), datetime.now(),
                    media.get("comments_count", None), media.get("like_count", None), media.get("media_url", None),
                    user_id, media.get("thumbnail_url", None), media.get("username", ""), datetime.now())
        cursor.execute(insert_query, values)
    except Exception as e:
        print(e, media)
        traceback.print_exc()
        pass
    finally:
        cursor.close()


def insert_user_detail_into_db(user, response):
    try:
        user_name = user.get("acc_name")
        print("\n user ID", response.get("id", ""), user_name)
        insert_user_by_id(response, user, user_name)
    except Exception as e:
        print(e, user_name)
        pass


def insert_user_by_id(response, user, user_name):
    cursor = get_insta_db_connection().cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    try:
        account_type = user.get("account_type")
        check_username = "SELECT username, reference_id FROM users u where username = '{username}'".format(username=user_name)
        cursor.execute(check_username)
        result = cursor.fetchone()
        user_user_name = result["username"] if result else None
        user_id = user.get("user_id") if user.get("user_id") else result["reference_id"] if result else None
        profile_picture_url = response.get("profile_picture_url", None)
        if user_user_name and user_user_name != response.get("username", ""):
            update_media_userid = "update media set user_id = null, username = '{updated_name}' where username = '{username}'".format(updated_name=user_name + "_old" , username=user_name)
            cursor.execute(update_media_userid)
        insert_query = '''INSERT INTO public.users (id, ig_id, website, username, biography, reference_id, account_type, follows_count,
                        media_count, followers_count, "name", profile_picture_url, last_updated, no_fb_response) 
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (username) DO UPDATE SET ig_id = %s, website=%s, biography=%s, reference_id=%s, account_type=%s, follows_count=%s,
                        media_count=%s, followers_count=%s, name=%s, profile_picture_url=%s, last_updated=%s, no_fb_response=%s'''
        
        val = (response.get("id", ""), response.get("ig_id", 0), response.get("website", ""), response.get("username", None), response.get("biography", None),
        user_id,account_type, response.get("follows_count", 0), response.get("media_count", 0), response.get("followers_count", 0), response.get("name", None), 
        profile_picture_url, datetime.now().isoformat(), False, response.get("ig_id", 0), response.get("website", ""),
        response.get("biography", None), user_id,account_type, response.get("follows_count", 0), response.get("media_count", 0), response.get("followers_count", 0),
        response.get("name", None), profile_picture_url, datetime.now().isoformat(), False)
        cursor.execute(insert_query, val)
    except Exception as e:
        print(e, user_name)
        insert_query = '''INSERT INTO public.users (id, ig_id, website, username, biography, reference_id, account_type, follows_count,
                        media_count, followers_count, "name", profile_picture_url, last_updated, no_fb_response)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO UPDATE SET username = %s, ig_id = %s, website=%s, biography=%s, reference_id=%s, account_type=%s, follows_count=%s,
                        media_count=%s, followers_count=%s, name=%s, profile_picture_url=%s, last_updated=%s, no_fb_response=%s'''
        
        val = (response.get("id", ""), response.get("ig_id", 0), response.get("website", ""), response.get("username", None), response.get("biography", None),
        user_id,account_type, response.get("follows_count", 0), response.get("media_count", 0), response.get("followers_count", 0), response.get("name", None), 
        profile_picture_url, datetime.now().isoformat(), False, response.get("username", None), response.get("ig_id", 0), response.get("website", ""),
        response.get("biography", None), user_id,account_type, response.get("follows_count", 0), response.get("media_count", 0), response.get("followers_count", 0),
        response.get("name", None), profile_picture_url, datetime.now().isoformat(), False)
        cursor.execute(insert_query, val)
    finally:
        update_last_update_time_social_account(user_name)
        cursor.close()
        pass


def update_insta_user_fb_response_status(user_name):
    ts_cur = get_insta_db_connection().cursor()
    try:
        query = "UPDATE users SET last_updated = %s, no_fb_response = %s WHERE username = %s"
        ts_cur.execute(query, (datetime.now(), True, user_name))
        print(ts_cur.rowcount, "timestamp updated")
    except Exception as e:
        traceback.print_exc()
        pass
    ts_cur.close()
