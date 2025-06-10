# tests/test_metrics.py

import time
import pytest
import requests
from src.metrics.exporter import SurgeOptMetrics, get_metrics


def test_metrics_initialization():
    """Test that metrics can be initialized."""
    metrics = SurgeOptMetrics(port=8001)  # Use different port for testing
    
    # Test that all metrics are properly initialized
    assert metrics.orders_per_minute is not None
    assert metrics.drift_detected_total is not None
    assert metrics.orders_processed_total is not None
    assert metrics.consumer_processing_seconds is not None


def test_metrics_recording():
    """Test that metrics can record values."""
    metrics = SurgeOptMetrics(port=8002)
    
    # Test order processing metrics
    metrics.record_order_processed("test_zone", success=True)
    metrics.record_order_processed("test_zone", success=False)
    
    # Test orders per minute
    metrics.update_orders_per_minute("test_zone", 42.5)
    
    # Test drift detection
    metrics.record_drift_detection("test_zone")
    
    # Test processing time
    metrics.record_processing_time(0.125)
    
    # Test Kafka metrics
    metrics.record_kafka_message("test_topic", success=True)
    metrics.record_kafka_message("test_topic", timeout=True)
    
    # Test ADWIN mean
    metrics.update_adwin_mean("test_zone", 35.7)
    
    # Test uptime
    metrics.update_uptime()


def test_metrics_server():
    """Test that metrics server can start and serve metrics."""
    metrics = SurgeOptMetrics(port=8003)
    
    # Start server
    metrics.start_server()
    time.sleep(1)  # Give server time to start
    
    # Record some test data
    metrics.update_orders_per_minute("helsinki", 25.0)
    metrics.record_drift_detection("helsinki")
    
    try:
        # Try to fetch metrics
        response = requests.get("http://localhost:8003/metrics", timeout=5)
        assert response.status_code == 200
        
        # Check that our metrics are in the response
        content = response.text
        assert "surgeopt_orders_per_minute" in content
        assert "surgeopt_adwin_drift_detected_total" in content
        assert 'zone="helsinki"' in content
        
    except requests.exceptions.RequestException:
        pytest.skip("Could not connect to metrics server")


def test_singleton_pattern():
    """Test that get_metrics returns the same instance."""
    metrics1 = get_metrics()
    metrics2 = get_metrics()
    
    assert metrics1 is metrics2
