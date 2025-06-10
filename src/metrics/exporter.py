# src/metrics/exporter.py

import time
import threading
from typing import Dict
from prometheus_client import Counter, Gauge, Histogram, start_http_server
from prometheus_client.core import CollectorRegistry


class SurgeOptMetrics:
    """
    Prometheus metrics collector for SurgeOpt.
    Exposes key business and system metrics for monitoring.
    """
    
    def __init__(self, port: int = 8000):
        self.port = port
        self.registry = CollectorRegistry()
        
        # Business Metrics
        self.orders_per_minute = Gauge(
            'surgeopt_orders_per_minute',
            'Current orders per minute by zone',
            ['zone'],
            registry=self.registry
        )
        
        self.drift_detected_total = Counter(
            'surgeopt_adwin_drift_detected_total',
            'Total number of ADWIN drift detections',
            ['zone'],
            registry=self.registry
        )
        
        self.orders_processed_total = Counter(
            'surgeopt_orders_processed_total',
            'Total orders processed by consumer',
            ['zone', 'status'],  # status: success, error
            registry=self.registry
        )
        
        # System Performance Metrics
        self.consumer_processing_seconds = Histogram(
            'surgeopt_consumer_processing_seconds',
            'Time spent processing each order message',
            registry=self.registry
        )
        
        self.kafka_messages_total = Counter(
            'surgeopt_kafka_messages_total',
            'Total Kafka messages received',
            ['topic', 'status'],  # status: success, error, timeout
            registry=self.registry
        )
        
        # ADWIN-specific metrics
        self.adwin_rolling_mean = Gauge(
            'surgeopt_adwin_rolling_mean',
            'Current ADWIN rolling mean by zone',
            ['zone'],
            registry=self.registry
        )
        
        # System health
        self.consumer_uptime_seconds = Gauge(
            'surgeopt_consumer_uptime_seconds',
            'Consumer uptime in seconds',
            registry=self.registry
                )
        
        self._start_time = time.time()
        self._server_thread = None
        
    def start_server(self, port: int = None) -> None:
        """Start the Prometheus metrics HTTP server in a background thread."""
        if port is not None:
            self.port = port
            
        if self._server_thread is not None:
            print(f"⚠️ Metrics server already running on port {self.port}")
            return
            
        try:
            self._server_thread = threading.Thread(
                target=self._run_server,
                daemon=True
            )
            self._server_thread.start()
            print(f"📊 Prometheus metrics server started on http://localhost:{self.port}/metrics")
        except Exception as e:
            print(f"❌ Failed to start metrics server: {e}")
            
    def _run_server(self) -> None:
        """Internal method to run the HTTP server."""
        start_http_server(self.port, registry=self.registry)
        
    def update_orders_per_minute(self, zone: str, count: float) -> None:
        """Update the orders per minute gauge for a zone."""
        self.orders_per_minute.labels(zone=zone).set(count)
        
    def record_drift_detection(self, zone: str) -> None:
        """Record when ADWIN detects drift in a zone."""
        self.drift_detected_total.labels(zone=zone).inc()
        
    def record_order_processed(self, zone: str, success: bool = True) -> None:
        """Record when an order is processed."""
        status = "success" if success else "error"
        self.orders_processed_total.labels(zone=zone, status=status).inc()
        
    def record_processing_time(self, duration_seconds: float) -> None:
        """Record how long it took to process a message."""
        self.consumer_processing_seconds.observe(duration_seconds)
        
    def record_kafka_message(self, topic: str, success: bool = True, timeout: bool = False) -> None:
        """Record Kafka message statistics."""
        if timeout:
            status = "timeout"
        elif success:
            status = "success"
        else:
            status = "error"
        self.kafka_messages_total.labels(topic=topic, status=status).inc()
        
    def update_adwin_mean(self, zone: str, mean: float) -> None:
        """Update the ADWIN rolling mean for a zone."""
        self.adwin_rolling_mean.labels(zone=zone).set(mean)
        
    def update_uptime(self) -> None:
        """Update the consumer uptime metric."""
        uptime = time.time() - self._start_time
        self.consumer_uptime_seconds.set(uptime)


# Global metrics instance (singleton pattern)
_metrics_instance = None

def get_metrics() -> SurgeOptMetrics:
    """Get the global metrics instance."""
    global _metrics_instance
    if _metrics_instance is None:
        _metrics_instance = SurgeOptMetrics()
    return _metrics_instance

def start_metrics_server(port: int = 8000) -> SurgeOptMetrics:
    """Initialize and start the metrics server."""
    metrics = get_metrics()
    metrics.port = port
    metrics.start_server()
    return metrics
