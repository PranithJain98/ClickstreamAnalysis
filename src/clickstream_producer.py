from kafka import KafkaProducer
import json
import time
import random

# Kafka Configuration
KAFKA_TOPIC = 'clickstream-events'
KAFKA_SERVER = 'localhost:9092'

# Initialize Kafka Producer
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Define User Actions
actions = ['click', 'view', 'add_to_cart', 'purchase']

def generate_clickstream_event():
    event = {
        'user_id': random.randint(1000, 9999),
        'session_id': random.randint(10000, 99999),
        'timestamp': int(time.time()),
        'action': random.choice(actions),
        'product_id': random.randint(1, 100),
    }
    return event

# Set the number of records to produce
num_records = 100

for _ in range(num_records):
    event = generate_clickstream_event()
    producer.send(KAFKA_TOPIC, event)
    print(f'Produced: {event}')
    time.sleep(random.uniform(0.1, 1.0))

print(f"Finished producing {num_records} records.")
