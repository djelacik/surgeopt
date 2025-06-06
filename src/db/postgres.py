# src/db/postgres.py

import psycopg2
from psycopg2.extras import execute_values
from typing import Dict, Any
import uuid
import datetime
import logging

# Setup basic logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# PostgreSQL connection settings (Docker default)
DB_CONFIG = {
    "host": "localhost",       # connects to Docker-mapped port
    "port": 5433,
    "dbname": "surgeopt",
    "user": "surgeopt",
    "password": "surgeopt"
}

def insert_order(order: Dict[str, Any]) -> None:
    """
    Inserts a single order into the 'orders' table in PostgreSQL.

    Args:
        order: Dict with keys 'order_id', 'lat', 'lon', 'timestamp' (Unix time)
    """
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                # Convert order_id to proper UUID format
                # order_id is like "order_7200", we'll generate a UUID from it
                order_id_str = order['order_id']
                order_number = order_id_str.replace('order_', '')
                # Pad to make a valid UUID format
                uuid_str = f"00000000-0000-0000-0000-{order_number.zfill(12)}"
                
                cur.execute(
                    """
                    INSERT INTO orders (order_id, lat, lon, timestamp)
                    VALUES (%s, %s, %s, to_timestamp(%s))
                    ON CONFLICT (order_id) DO NOTHING;
                    """,
                    (
                        uuid_str,  # Use string instead of UUID object
                        order["lat"],
                        order["lon"],
                        order["timestamp"]
                    )
                )
                logger.info(f"✅ Inserted order {order['order_id']} -> {uuid_str}")
    except Exception as e:
        logger.error(f"❌ Failed to insert order {order.get('order_id', 'unknown')}: {e}")
