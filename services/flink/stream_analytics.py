import json
import threading
import time
from collections import defaultdict
from kafka import KafkaConsumer

# Простой real-time аналитик на Python
# (PyFlink Kafka коннектор требует точного совпадения версий JAR)

consumer = KafkaConsumer(
    'ecom.user-events',
    bootstrap_servers='localhost:29092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='latest',
    group_id='flink-analytics'
)

# Счётчики за последние 60 секунд
event_counts = defaultdict(int)
product_counts = defaultdict(int)
revenue = 0.0
total_events = 0

def print_stats():
    while True:
        time.sleep(10)
        print("\n" + "="*50)
        print(f"  EcomFlow Real-time Analytics (last 10 sec)")
        print("="*50)
        print(f"  Total events:   {total_events}")
        print(f"  Revenue:        ${revenue:.2f}")
        print(f"\n  Events by type:")
        for k, v in sorted(event_counts.items()):
            print(f"    {k:15} {v}")
        print(f"\n  Top products:")
        top = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        for k, v in top:
            print(f"    {k:15} {v}")
        print("="*50)
        event_counts.clear()
        product_counts.clear()

# Запускаем вывод статистики в фоне
t = threading.Thread(target=print_stats, daemon=True)
t.start()

print("EcomFlow Stream Analytics started!")
print("Stats will appear every 10 seconds...\n")

for message in consumer:
    event = message.value
    total_events += 1
    event_counts[event['event_type']] += 1
    product_counts[event['product']] += 1
    if event['event_type'] == 'purchase':
        revenue += event['price'] * event['quantity']
