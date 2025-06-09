"""Basic tests that don't require external services."""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def test_python_version():
    """Test that we're running a supported Python version."""
    assert sys.version_info >= (3, 8), "Python 3.8+ required"


def test_imports():
    """Test that our modules can be imported."""
    try:
        from db.postgres import insert_order, DB_CONFIG
        from consumer.consumer import start_consumer
        from simulator.producer import generate_order, simulate_orders
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


def test_environment_variables():
    """Test that environment variables are being read correctly."""
    from db.postgres import DB_CONFIG
    
    # In CI, these should be set
    expected_values = {
        'host': 'localhost',
        'user': 'surgeopt',
        'password': 'surgeopt',
        'dbname': 'surgeopt'
    }
    
    # Only check if we're in CI (environment variables are set)
    if os.getenv('POSTGRES_HOST'):
        for key, expected in expected_values.items():
            assert DB_CONFIG[key] == expected, f"Expected {key}={expected}, got {DB_CONFIG[key]}"
        
        # Port can be either 5432 (CI) or 5433 (local development)
        assert DB_CONFIG['port'] in [5432, 5433], f"Expected port to be 5432 or 5433, got {DB_CONFIG['port']}"


def test_order_generation():
    """Test that we can generate valid orders."""
    from simulator.producer import generate_order
    
    order = generate_order("Kallio")  # Need to provide a zone parameter
    
    assert 'order_id' in order
    assert 'lat' in order
    assert 'lon' in order
    assert 'timestamp' in order
    assert 'zone' in order
    
    assert isinstance(order['lat'], (int, float))
    assert isinstance(order['lon'], (int, float))
    assert isinstance(order['timestamp'], (int, float))
    assert isinstance(order['order_id'], str)
    assert isinstance(order['zone'], str)
    
    # Check coordinate ranges (Helsinki area)
    assert 59.5 <= order['lat'] <= 61.0
    assert 23.0 <= order['lon'] <= 26.0
    assert order['zone'] == "Kallio"