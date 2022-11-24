from scripts.excel_usernames import usernames_list
from scripts.excel_users_dict import users_dict
from utils.db_utils import get_insta_db_connection

def in_query(item_list):
    in_query = ''
    for idx, item in enumerate(item_list):
        if not idx:
            in_query += f"'{item}'"
        else:
            in_query += ", " + f"'{item}'"
    return in_query

def check_users():
    username_list_str = in_query(usernames_list)
    # query = f"""
    #     select count(username) from public.users
    # """
    query = f"""
        select username from public.users
        where username in ({username_list_str})
    """
    cursor = get_insta_db_connection().cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    # print(result)
    sql_set = {tup[0] for tup in result}
    # print(sql_set)
    username_set = set(usernames_list)
    not_in_db_set = username_set - sql_set
    print(len(not_in_db_set))
    for user in not_in_db_set:
        print(f"'{user}': '{users_dict[user]}',")