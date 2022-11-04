import traceback
import psycopg2.extras
from datetime import datetime
from utils.db_utils import get_rewards_db_connection


def get_new_users():
    query = "SELECT distinct sa.id, TRIM(sa.acc_name) as acc_name, sa.user_id, sa.account_type \
            FROM social_accounts sa \
            WHERE platform_name = 'instagram' \
            AND acc_name IS NOT NULL AND acc_name <> '' AND acc_name <> ' ' \
            AND social_user_last_update IS NULL \
            AND (no_fb_response = false OR no_fb_response IS NULL)"
    cursor = get_rewards_db_connection().cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    user_names = set()
    insta_usernames = list()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        parse_resultset(rows, insta_usernames, user_names)
    except Exception as e:
        traceback.print_exc()
        pass
    finally:
        cursor.close()
        get_rewards_db_connection().close()
    return insta_usernames


def parse_resultset(rows, insta_usernames, user_names):
    for row in rows:
        acc_name = row.get("acc_name").strip()
        if acc_name and acc_name not in user_names:
            insta_usernames.append({"acc_name": acc_name,
            "user_id": row.get("user_id", "").strip(),
            "account_type": row.get("account_type", None),
            "id": row.get("id", "")
            })
            user_names.add(acc_name)


def update_last_update_time_social_account(acc_name):
    ts_cur = get_rewards_db_connection().cursor()
    query = "UPDATE social_accounts SET social_user_last_update = %s, no_fb_response = FALSE WHERE platform_name = 'instagram' AND acc_name = %s"
    ts_cur.execute(query, (datetime.now(), acc_name))
    print(ts_cur.rowcount, "timestamp updated")
    ts_cur.close()


def update_rewards_user_profile_status(acc_name):
    ts_cur = get_rewards_db_connection().cursor()
    query = "UPDATE social_accounts SET social_user_last_update = %s, no_fb_response = TRUE WHERE platform_name = 'instagram' AND acc_name = %s"
    ts_cur.execute(query, (datetime.now(), acc_name))
    print(ts_cur.rowcount, "social_accounts timestamp updated")
    ts_cur.close()
