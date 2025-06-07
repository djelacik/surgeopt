# tests/test_postgres.py

import psycopg2
import pytest

from src.db.postgres import DB_CONFIG, insert_order


def test_insert_order():
    """Test that insert_order works with a simple order"""
    test_order = {
        "order_id": "order_9999",
        "lat": 60.1234,
        "lon": 24.5678,
        "timestamp": 1722000000.0
    }
    
    # Insert the order (function handles its own connection)
    insert_order(test_order)
    
    # Verify it was inserted by checking the database
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            # Expected UUID format: 00000000-0000-0000-0000-000000009999
            expected_uuid = "00000000-0000-0000-0000-000000009999"
            cur.execute("SELECT lat, lon FROM orders WHERE order_id = %s", [expected_uuid])
            result = cur.fetchone()
            
            assert result is not None, "Order was not inserted"
            assert result[0] == test_order["lat"], "Latitude doesn't match"
            assert result[1] == test_order["lon"], "Longitude doesn't match"

def test_insert_duplicate_order():
    """Test that inserting the same order_id twice does not raise an error or duplicate data"""
    test_order = {
        "order_id": "order_9999",
        "lat": 60.1234,
        "lon": 24.5678,
        "timestamp": 1722000000.0
    }

    insert_order(test_order)  # First insert
    insert_order(test_order)  # Duplicate insert

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM orders WHERE order_id = %s", ["00000000-0000-0000-0000-000000009999"])
            count = cur.fetchone()[0]
            assert count == 1, f"Expected 1 record, got {count}"

def test_insert_invalid_order_id():
    """Test that non-numeric order_id raises ValueError"""
    bad_order = {
        "order_id": "not_a_number",
        "lat": 60.0,
        "lon": 24.0,
        "timestamp": 1722000000.0
    }

    with pytest.raises(ValueError):
        insert_order(bad_order)

@pytest.fixture(autouse=True)
def cleanup_test_order():
    yield
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM orders WHERE order_id = %s", ["00000000-0000-0000-0000-000000009999"])
            conn.commit()
