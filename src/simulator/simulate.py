# src/simulator/simulate.py
# This script simulates the generation of order events and sends them to a Kafka topic.

from confluent_kafka import Producer
import json
import time
import random

# Configure the producer
producer = Producer({
    'bootstrap.servers': 'localhost:9092'
})

def delivery_report(err, msg):
    """Called once for each message produced to indicate delivery result."""
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

while True:
    order = {
        "order_id": f"order_{random.randint(1000, 9999)}",
        "lat": random.uniform(60.15, 60.25),
        "lon": random.uniform(24.80, 24.95),
        "timestamp": time.time()
    }
    
    # Send the message
    producer.produce(
        'order_created', 
        value=json.dumps(order).encode('utf-8'),
        callback=delivery_report
    )
    
    # Wait for any outstanding messages to be delivered
    producer.poll(0)
    
    print("Sent:", order)
    time.sleep(1)