# src/db/postgres.py

import datetime
import logging
import uuid
from typing import Any, Dict

import psycopg2
from psycopg2.extras import execute_values

# Setup basic logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# PostgreSQL connection settings (Docker default)
import os

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", "5433")),  # Default to 5433 for local
    "dbname": os.getenv("POSTGRES_DB", "surgeopt"),
    "user": os.getenv("POSTGRES_USER", "surgeopt"),
    "password": os.getenv("POSTGRES_PASSWORD", "surgeopt"),
}


def insert_order(order: Dict[str, Any]) -> None:
    """
    Inserts a single order into the 'orders' table in PostgreSQL.

    Args:
        order: Dict with keys 'order_id', 'lat', 'lon', 'timestamp' (Unix time)

    Raises:
        ValueError: if order_id is not in the format 'order_<int>'
        Exception: if database insertion fails
    """
    try:
        # Validate and parse order_id
        order_id_str = order["order_id"]
        if not order_id_str.startswith("order_"):
            raise ValueError(f"Invalid order_id format: {order_id_str}")

        try:
            order_number = int(order_id_str.replace("order_", ""))
        except ValueError:
            raise ValueError(f"Order ID must end with an integer: {order_id_str}")

        # Generate UUID-like padded string
        uuid_str = f"00000000-0000-0000-0000-{str(order_number).zfill(12)}"

        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO orders (order_id, lat, lon, timestamp)
                    VALUES (%s, %s, %s, to_timestamp(%s))
                    ON CONFLICT (order_id) DO NOTHING;
                    """,
                    (
                        uuid_str,  # Keep as string for PostgreSQL
                        order["lat"],
                        order["lon"],
                        order["timestamp"],
                    ),
                )
                logger.info(f"✅ Inserted order {order_id_str} -> {uuid_str}")

    except Exception as e:
        logger.error(
            f"❌ Failed to insert order {order.get('order_id', 'unknown')}: {e}"
        )
        raise  # Re-raise so that tests can catch it
