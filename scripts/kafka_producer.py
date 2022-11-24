import requests
import json
import traceback
import time
from flask import current_app
from kafka import KafkaProducer


def send_to_insta_kafka(payload,key):
    try:
        event={}
        event['payload'] = payload
        producer = KafkaProducer(bootstrap_servers= current_app.config['KAFKA_SERVER'], acks = 1, request_timeout_ms = 150)
        # producer.send(current_app.config['TEST_TOPIC'], value= json.dumps(payload).encode('utf-8'))
        producer.send(current_app.config['SCRAPER_KAFKA_TOPIC'], key=key.encode('utf-8'), value= json.dumps(payload).encode('utf-8'))
        print('inserted into kafka ----')
    except Exception:
        traceback.print_exc()
