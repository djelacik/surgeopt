# src/simulator/simulate.py
# This script simulates the generation of order events and sends them to a Kafka topic.

import json
import random
import time

from confluent_kafka import Producer


def get_producer(bootstrap_servers="localhost:9092"):
    """Create and return a Kafka producer."""
    return Producer({"bootstrap.servers": bootstrap_servers})


def delivery_report(err, msg):
    """Called once for each message produced to indicate delivery result."""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def generate_order():
    """Generate a single order with random data."""
    return {
        "order_id": f"order_{random.randint(1000, 9999)}",
        "lat": random.uniform(60.15, 60.25),
        "lon": random.uniform(24.80, 24.95),
        "timestamp": time.time(),
    }


def publish_order(producer, order, topic="order_created"):
    """Publish a single order to Kafka."""
    producer.produce(
        topic,
        value=json.dumps(order).encode("utf-8"),
        callback=delivery_report,
    )
    # Wait for any outstanding messages to be delivered
    producer.poll(0)


def simulate_orders(bootstrap_servers="localhost:9092", topic="order_created", count=None):
    """Simulate order generation and publishing."""
    producer = get_producer(bootstrap_servers)
    
    orders_sent = 0
    while count is None or orders_sent < count:
        order = generate_order()
        
        # Send the message
        publish_order(producer, order, topic)
        
        print(f"📦 Sent order: {order}")
        
        orders_sent += 1
        time.sleep(1)  # Wait 1 second between messages


if __name__ == "__main__":
    # Only run the simulation if this file is executed directly
    simulate_orders()
