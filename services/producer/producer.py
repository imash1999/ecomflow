import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer

# Подключение к Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Тестовые данные
USERS = [1, 2, 3]
PRODUCTS = [
    {'id': 'prod-001', 'name': 'Laptop Stand',  'price': 250.00},
    {'id': 'prod-002', 'name': 'USB Hub',        'price': 100.00},
    {'id': 'prod-003', 'name': 'Mouse',           'price': 34.05},
    {'id': 'prod-004', 'name': 'Keyboard',        'price': 89.99},
    {'id': 'prod-005', 'name': 'Monitor 27"',    'price': 700.00},
]
EVENT_TYPES = ['view', 'click', 'add_to_cart', 'purchase']

def generate_event():
    product = random.choice(PRODUCTS)
    return {
        'event_type': random.choice(EVENT_TYPES),
        'user_id':    random.choice(USERS),
        'product_id': product['id'],
        'product':    product['name'],
        'price':      product['price'],
        'quantity':   random.randint(1, 5),
        'timestamp':  datetime.utcnow().isoformat()
    }

print('🚀 Producer started! Sending events to Kafka...')
print('   Press Ctrl+C to stop\n')

count = 0
while True:
    event = generate_event()
    producer.send('ecom.user-events', value=event)
    count += 1
    print(f'[{count}] {event["event_type"]:12} | user={event["user_id"]} | {event["product"]:15} | ${event["price"]}')
    time.sleep(1)
