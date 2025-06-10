# src/consumer/consumer.py

import json
import time
import uuid
from typing import Dict
from confluent_kafka import Consumer, KafkaException, KafkaError, Producer
from src.db.postgres import insert_order
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
from src.adwin.detector import DriftDetector
from src.metrics.exporter import get_metrics

# --- Global state ---
order_buffer = defaultdict(lambda: deque(maxlen=300))  # ~5 min buffer @1Hz
adwin = DriftDetector()
producer = Producer({"bootstrap.servers": "localhost:9092"})
metrics = get_metrics()  # Initialize Prometheus metrics


def update_zone_orders(zone: str, timestamp: float) -> None:
    """
    Add new timestamp to zone-specific order buffer.
    """
    order_buffer[zone].append(datetime.fromtimestamp(timestamp))


def compute_orders_per_minute(zone: str) -> float:
    """
    Compute number of orders in the past 60s for a given zone.
    """
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(seconds=60)
    return sum(1 for t in order_buffer[zone] if t >= window_start)


def send_gap_detected(zone: str, orders_per_min: float, mean: float) -> None:
    """
    Send a Kafka message to gap_detected topic when ADWIN detects drift.
    """
    message = {
        "zone": zone,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "orders_per_minute": orders_per_min,
        "rolling_mean": mean,
    }
    print(f"📣 gap_detected! Zone={zone}, Orders/min={orders_per_min:.1f}, Mean={mean:.1f}")
    producer.produce("gap_detected", json.dumps(message).encode("utf-8"))
    producer.flush()
    print(f"📣 gap_detected → {message}")


def start_consumer(
    topic: str = "order_created", bootstrap_servers: str = "localhost:9092"
):
    """
    Listens to Kafka topic and inserts incoming order messages into PostgreSQL.
    Tracks order frequency per zone and publishes gap_detected if ADWIN detects drift.
    """
    print("🔄 Starting consumer...")
    
    # Start metrics server
    metrics.start_server()

    consumer = Consumer(
        {
            "bootstrap.servers": bootstrap_servers,
            "group.id": "order-consumer-group",
            "auto.offset.reset": "earliest",
            "enable.auto.commit": True,
            "session.timeout.ms": 6000,
            "heartbeat.interval.ms": 2000,
        }
    )

    print(f"🔗 Subscribing to topic '{topic}'")
    consumer.subscribe([topic])

    last_checked = datetime.now(timezone.utc)

    try:
        while True:
            # Record uptime
            metrics.update_uptime()
            
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                metrics.record_kafka_message(topic, timeout=True)
                continue

            if msg.error():
                if msg.error().code() != KafkaError._PARTITION_EOF:
                    print(f"❌ Kafka error: {msg.error()}")
                    metrics.record_kafka_message(topic, success=False)
                continue

            # Record successful Kafka message
            metrics.record_kafka_message(topic, success=True)
            
            # Measure processing time
            processing_start = time.time()
            
            try:
                order = json.loads(msg.value().decode("utf-8"))
                print(f"📦 Received: {order}")

                insert_order(order)

                # Example zone assignment (replace with real logic later)
                zone = order.get("zone", "default")
                timestamp = order["timestamp"]

                update_zone_orders(zone, timestamp)
                
                # Record successful order processing
                metrics.record_order_processed(zone, success=True)

                # Every 60 seconds, evaluate ADWIN per zone
                now = datetime.now(timezone.utc)
                if (now - last_checked).total_seconds() >= 60:
                    for z in order_buffer:
                        opm = compute_orders_per_minute(z)
                        drift, mean = adwin.update(z, opm)
                        
                        # Update metrics
                        metrics.update_orders_per_minute(z, opm)
                        metrics.update_adwin_mean(z, mean)
                        
                        if drift:
                            send_gap_detected(z, opm, mean)
                            # Record drift detection
                            metrics.record_drift_detection(z)
                    last_checked = now
                    
                # Record processing time
                processing_duration = time.time() - processing_start
                metrics.record_processing_time(processing_duration)

            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"⚠️ Failed to process message: {e}")
                # Record failed order processing
                zone = "unknown"
                metrics.record_order_processed(zone, success=False)
                continue

    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")

    finally:
        print("🧹 Closing consumer...")
        consumer.close()


if __name__ == "__main__":
    print("🚀 Starting SurgeOpt Consumer...")
    start_consumer()
