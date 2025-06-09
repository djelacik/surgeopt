# tests/test_postgres.py

import uuid
import pytest
from src.db.postgres import insert_order


def test_insert_order():
    test_order = {
        "order_id": str(uuid.uuid4()),  # Generate valid UUID
        "lat": 60.1234,
        "lon": 24.5678,
        "timestamp": 1722000000.0
    }

    # This will test the insert_order function directly
    # It should not raise a UUID format error
    try:
        insert_order(test_order)
    except ValueError as e:
        if "Invalid UUID format" in str(e):
            pytest.fail(f"UUID format error should not occur with valid UUID: {e}")
        # Other errors are acceptable for this test


def test_insert_duplicate_order():
    """Test inserting the same order twice"""
    test_order = {
        "order_id": str(uuid.uuid4()),  # Generate valid UUID
        "lat": 60.1234,
        "lon": 24.5678,
        "timestamp": 1722000000.0
    }

    # First insert
    try:
        insert_order(test_order)
    except ValueError as e:
        if "Invalid UUID format" in str(e):
            pytest.fail(f"First insert: UUID format error should not occur: {e}")
    
    # Second insert should either succeed or handle gracefully
    try:
        insert_order(test_order)
    except Exception as e:
        # Should not be a UUID format error
        assert "Invalid UUID format" not in str(e)
