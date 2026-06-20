import json
from kafka import KafkaConsumer
import psycopg2

# Подключение к Kafka
consumer = KafkaConsumer(
    'ecom.user-events',
    bootstrap_servers='localhost:29092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='latest',
    group_id='ecomflow-consumer'
)

# Подключение к PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="ecomflow",
    user="ecom_user",
    password="ecom_pass"
)
cur = conn.cursor()

print("Consumer started! Listening to ecom.user-events...")
print("Press Ctrl+C to stop\n")

count = 0
for message in consumer:
    event = message.value
    count += 1

    # Записываем только purchase события в PostgreSQL
    if event['event_type'] == 'purchase':
        cur.execute("""
            INSERT INTO order_items (order_id, product_id, name, price, quantity)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (1, event['product_id'], event['product'], event['price'], event['quantity']))
        conn.commit()
        print(f"[{count}] PURCHASE saved -> {event['product']} x{event['quantity']} ${event['price']}")
    else:
        print(f"[{count}] {event['event_type']:12} | {event['product']:15} | user={event['user_id']}")
