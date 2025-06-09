# src/simulator/producer.py

import json
import time
import random
import uuid
import argparse
from datetime import datetime
from confluent_kafka import Producer


ZONES = {
    "Kallio": {"lat_range": (60.185, 60.195), "lon_range": (24.94, 24.97)},
    "Kamppi": {"lat_range": (60.165, 60.175), "lon_range": (24.91, 24.94)},
    "Pasila": {"lat_range": (60.200, 60.210), "lon_range": (24.92, 24.96)},
}

producer = Producer({"bootstrap.servers": "localhost:9092"})


def generate_order(zone: str) -> dict:
    lat = round(random.uniform(*ZONES[zone]["lat_range"]), 6)
    lon = round(random.uniform(*ZONES[zone]["lon_range"]), 6)
    return {
        "order_id": str(uuid.uuid4()),
        "lat": lat,
        "lon": lon,
        "timestamp": time.time(),
        "zone": zone,
    }


def simulate_orders(burst_zone: str, burst_start: int, burst_rate: int, duration: int):
    """
    Simulates normal and burst order traffic into Kafka.
    """
    print(f"🚀 Starting simulation for {duration}s...")
    print(f"💥 Burst in zone '{burst_zone}' at t={burst_start}s with {burst_rate} extra orders")

    for i in range(duration):
        # normaalitilanne
        for zone in ZONES:
            order = generate_order(zone)
            producer.produce("order_created", json.dumps(order).encode("utf-8"))
            print(f"📤 Sent: {order}")

        # burst-hetki
        if i == burst_start:
            print(f"🔥 Triggering burst in {burst_zone}")
            for _ in range(burst_rate):
                order = generate_order(burst_zone)
                producer.produce("order_created", json.dumps(order).encode("utf-8"))
                print(f"🔥 Burst Sent: {order}")

        producer.flush()
        time.sleep(1)

    print("✅ Simulation complete.")


if __name__ == "__main__":
    # Command line arguments for burst simulation control:
    # --burst_zone: Which zone gets extra orders (Kallio/Kamppi/Pasila)
    # --burst_start: When burst happens (seconds after start)
    # --burst_rate: How many extra orders during burst
    # --duration: Total simulation time in seconds
    # Example: python producer.py --burst_zone Kamppi --burst_start 45 --burst_rate 30
    parser = argparse.ArgumentParser(description="Simulate Kafka orders with optional burst.")
    parser.add_argument("--burst_zone", type=str, default="Kallio", choices=ZONES.keys())
    parser.add_argument("--burst_start", type=int, default=30, help="Seconds after which burst occurs")
    parser.add_argument("--burst_rate", type=int, default=5, help="How many extra orders during burst")
    parser.add_argument("--duration", type=int, default=90, help="Total duration of simulation in seconds")

    args = parser.parse_args()

    simulate_orders(
        burst_zone=args.burst_zone,
        burst_start=args.burst_start,
        burst_rate=args.burst_rate,
        duration=args.duration,
    )