from utils.db_utils import get_insta_db_connection
import pandas as pd
from datetime import datetime

def insert_media_details_in_db(file_name):
	cursor = get_insta_db_connection().cursor()
	try:
		df = pd.read_excel(file_name, engine='openpyxl')
		for index, row in df.iterrows():
			query = """INSERT INTO public.scrape_media
						(username, media_url, shortcode, comments_count, like_count, view_count, mm_user_id, updated_date)
						VALUES(%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (shortcode, updated_date) DO NOTHING"""
			values = (row["user_name"], row["media_url"], row["shortcode"], row["comments_count"], row["like_count"], row["view_count"], row["user_id"], datetime.now().date())
			cursor = get_insta_db_connection().cursor()
			cursor.execute(query, values)
			# print(cursor.rowcount, " media inserted.")
			cursor.close()
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		get_insta_db_connection().close()