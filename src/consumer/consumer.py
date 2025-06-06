import json
import uuid
from typing import Dict

from confluent_kafka import Consumer, KafkaException
from src.db.postgres import insert_order


def start_consumer(topic: str = "order_created", bootstrap_servers: str = "localhost:9092"):
    """
    Listens to Kafka topic and inserts incoming order messages into PostgreSQL.
    """
    print("🔄 Starting consumer...")

    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'order-consumer-group',  # Fixed group ID
        'auto.offset.reset': 'earliest',  # Read from beginning
        'enable.auto.commit': True,
        'session.timeout.ms': 6000,
        'heartbeat.interval.ms': 2000
    })

    print(f"🔗 Subscribing to topic '{topic}'")
    consumer.subscribe([topic])

    try:
        while True:
            print("⏳ Polling Kafka...")
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                print("… No message yet")
                continue

            if msg.error():
                print(f"❌ Kafka error: {msg.error()}")
                continue

            order = json.loads(msg.value().decode('utf-8'))
            print(f"📦 Received: {order}")
            insert_order(order)

    except KeyboardInterrupt:
        print("\n[!] Stopped by user")

    finally:
        print("🛑 Closing consumer...")
        consumer.close()


if __name__ == "__main__":
    start_consumer()
