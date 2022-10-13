# import json

# from kafka import KafkaConsumer, KafkaProducer

# from app import config


# def get_kafka_consumer():
#     consumer = KafkaConsumer(
#         auto_offset_reset=config.KAFKA_AUTO_OFFSET_RESET,
#         bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS
#     )
#     return consumer


# def get_kafka_producer():
#     producer = KafkaProducer(
#         bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
#         acks=1,
#         request_timeout_ms=3000
#     )
#     return producer


# def send_to_producer(topic_list, kafka_data):
#     producer = get_kafka_producer()
#     producer.send(topic_list, json.dumps(kafka_data).encode('utf-8'))