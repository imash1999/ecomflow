import json
import uuid
from datetime import datetime
from kafka import KafkaConsumer
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Подключение к Kafka
consumer = KafkaConsumer(
    'ecom.user-events',
    bootstrap_servers='localhost:29092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='latest',
    group_id='cassandra-consumer'
)

# Подключение к Cassandra
cluster = Cluster(['localhost'], port=9042)
session = cluster.connect('ecomflow')

# Подготовленный запрос
insert = session.prepare("""
    INSERT INTO user_events
    (event_id, user_id, event_type, product_id, product, price, quantity, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""")

print("Kafka -> Cassandra pipeline started!")
print("Press Ctrl+C to stop\n")

count = 0
for message in consumer:
    event = message.value
    count += 1

    session.execute(insert, (
        uuid.uuid4(),
        event['user_id'],
        event['event_type'],
        event['product_id'],
        event['product'],
        event['price'],
        event['quantity'],
        datetime.utcnow()
    ))

    print(f"[{count}] saved -> {event['event_type']:12} | {event['product']:15} | user={event['user_id']}")
