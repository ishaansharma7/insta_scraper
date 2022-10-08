import os
import psycopg2


def get_insta_db_connection(application_name="insta_data_script"):
    insta_connection = psycopg2.connect(host=os.getenv("SQL_HOST"),
                database=os.getenv("SQL_DATABASE"),
                user=os.getenv("SQL_USER_NAME"),
                password=os.getenv("SQL_PASSWORD"),
                port=os.getenv("PSQL_PORT"),
                application_name=application_name)
    insta_connection.autocommit = True
    return insta_connection


def get_rewards_db_connection(application_name="insta_data_script"):
    rewards_conn = psycopg2.connect(host=os.getenv("REWARDS_IP"),
                            database=os.getenv("REWARDS_DB"),
                            user=os.getenv("REWARDS_USER"),
                            password=os.getenv("REWARDS_PASS"),
                            port=os.getenv("PSQL_PORT"),
                            application_name=application_name)
    rewards_conn.autocommit = True
    return rewards_conn


def get_campaigns_user_db_connection(application_name="insta_data_script"):
    campaigns_conn = psycopg2.connect(host=os.getenv("CAMPAIGNS_IP"),
                                    database=os.getenv("CAMPAIGNS_DB"),
                                    user=os.getenv("CAMPAIGNS_USER"),
                                    password=os.getenv("CAMPAIGNS_PASS"),
                                    port=os.getenv("CAMPAIGNS_PORT"),
                                    application_name=application_name)
    campaigns_conn.autocommit = True
    return campaigns_conn
