# src/consumer/consumer.py

import json
from typing import Dict
from confluent_kafka import Consumer, KafkaException, KafkaError, Producer
from src.db.postgres import insert_order
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
from src.adwin.detector import DriftDetector

# --- Global state ---
order_buffer = defaultdict(lambda: deque(maxlen=300))  # ~5 min buffer @1Hz
adwin = DriftDetector(delta=0.01)  # Less sensitive for more obvious spikes
producer = Producer({"bootstrap.servers": "localhost:9092"})


def update_zone_orders(zone: str, timestamp: float) -> None:
    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    order_buffer[zone].append(dt)


def compute_orders_per_minute(zone: str) -> float:
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(seconds=60)
    return sum(1 for t in order_buffer[zone] if t >= window_start)


def send_gap_detected(zone: str, orders_per_min: float, mean: float) -> None:
    message = {
        "zone": zone,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "orders_per_minute": orders_per_min,
        "rolling_mean": mean,
    }
    print(f"📤 Sent alert to 'gap_detected' topic")
    producer.produce("gap_detected", json.dumps(message).encode("utf-8"))
    producer.flush()


def start_consumer(topic: str = "order_created", bootstrap_servers: str = "localhost:9092"):
    print("🔄 Starting consumer...")

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
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() != KafkaError._PARTITION_EOF:
                    print(f"❌ Kafka error: {msg.error()}")
                continue

            try:
                order = json.loads(msg.value().decode("utf-8"))

                # Poimi tarvittavat kentät
                zone = order.get("zone", "default")
                timestamp = order["timestamp"]

                # Tulosta jokainen tilaus ja sen timestamp
                print(f"📦 {zone:<7} {datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%H:%M:%S')}")

                # Päivitä bufferi ja laske tilaukset
                update_zone_orders(zone, timestamp)
                opm = compute_orders_per_minute(zone)

                # ADWIN drift detection
                drift, mean = adwin.update(zone, opm)
                print(f"   🔎 {zone:<7} | OPM={opm:5.1f} | Mean={mean:5.1f} | Drift={drift}")

                if drift:
                    print(f"🚨 SPIKE DETECTED in {zone}: {opm:.1f} orders/min (baseline: {mean:.1f})")
                    send_gap_detected(zone, opm, mean)

                # Tallenna tietokantaan
                try:
                    insert_order(order)
                except Exception as e:
                    print(f"❌ DB Error: {e}")

                # Yhteenveto 60s välein
                now = datetime.now(timezone.utc)
                if (now - last_checked).total_seconds() >= 60:
                    print(f"\n📊 SYSTEM STATUS at {now.strftime('%H:%M:%S')} 📊")
                    total_orders = 0
                    for z in order_buffer:
                        zone_opm = compute_orders_per_minute(z)
                        total_orders += zone_opm
                        print(f"   {z}: {zone_opm:.0f} orders/min")
                    print(f"   Total: {total_orders:.0f} orders/min across all zones")
                    print("─" * 50)
                    last_checked = now

            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"⚠️ Failed to process message: {e}")
                continue

    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")

    finally:
        print("🧹 Closing consumer...")
        consumer.close()


if __name__ == "__main__":
    print("🚀 Starting SurgeOpt Consumer...")
    start_consumer()
