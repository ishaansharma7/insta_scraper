from kafka import KafkaProducer
from dotenv import load_dotenv
import os
import json
import traceback


load_dotenv()

def send_to_scraper_kafka(payload):
    try:
        event={}
        event['payload'] = payload
        producer = KafkaProducer(bootstrap_servers= os.environ['KAFKA_SERVER'], acks = 1, request_timeout_ms = 150)
        producer.send(os.environ['SCRAPER_KAFKA_TOPIC'], value= json.dumps(payload).encode('utf-8'))
    except Exception:
        traceback.print_exc()

#   {'user_name':'harshit.tewatia', 'user_id':''}


def send_lost_users_to_kafka(lost_users_perm):
    print('send_lost_users_to_kafka -----')
    for key, value in lost_users_perm.items():
        send_to_scraper_kafka({'user_name': key, 'user_id': value})
        print({'user_name': key, 'user_id': value})
    lost_users_perm.clear()
