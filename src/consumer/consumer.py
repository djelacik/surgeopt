import json
from confluent_kafka import Consumer, KafkaException
from typing import List, Dict


def start_consumer(topic: str = "order_created", bootstrap_servers: str = "localhost:9092"):
    """
    Listens to Kafka topic and stores messages in a list.
    """
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test-consumer-group',
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe([topic])
    print(f"[✓] Listening to topic '{topic}'")

    orders: List[Dict] = []

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())

            order = json.loads(msg.value().decode('utf-8'))
            print(f"📦 Received: {order}")
            orders.append(order)

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")

    finally:
        consumer.close()
        print("[✓] Kafka consumer closed.")

    return orders


if __name__ == "__main__":
    start_consumer()
