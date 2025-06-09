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
        ValueError: if order_id is not a valid UUID format
        Exception: if database insertion fails
    """
    try:
        # Validate order_id as UUID
        order_id_str = order["order_id"]
        try:
            # This will raise ValueError if not a valid UUID
            uuid.UUID(order_id_str)
        except ValueError:
            raise ValueError(f"Invalid UUID format: {order_id_str}")

        # Insert into database
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO orders (order_id, lat, lon, timestamp)
                    VALUES (%s, %s, %s, to_timestamp(%s))
                    ON CONFLICT (order_id) DO NOTHING;
                    """,
                    (
                        order_id_str,  # Keep as string for PostgreSQL
                        order["lat"],
                        order["lon"],
                        order["timestamp"],
                    ),
                )
        # Silently insert order (only log errors)
        pass

    except Exception as e:
        logger.error(
            f"❌ Failed to insert order {order.get('order_id', 'unknown')}: {e}"
        )
        raise  # Re-raise so that tests can catch it
