import os
import psycopg2
from constants import SQL_HOST,PSQL_PORT,SQL_DATABASE,SQL_USER_NAME,SQL_PASSWORD,REWARDS_IP,REWARDS_PASS,REWARDS_DB,REWARDS_USER


def get_insta_db_connection():
    insta_connection = psycopg2.connect(host=SQL_HOST,
                database=SQL_DATABASE,
                user=SQL_USER_NAME,
                password=SQL_PASSWORD,
                port=PSQL_PORT)
    insta_connection.autocommit = True
    return insta_connection


def get_rewards_db_connection():
    rewards_conn = psycopg2.connect(host=REWARDS_IP,
                            database=REWARDS_DB,
                            user=REWARDS_USER,
                            password=REWARDS_PASS,
                            port=PSQL_PORT)
    rewards_conn.autocommit = True
    return rewards_conn