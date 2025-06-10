# SurgeOpt Monitoring System

This document describes the Prometheus and Grafana monitoring setup for the SurgeOpt project.

## Overview

The SurgeOpt monitoring system provides comprehensive observability for:
- **Business Metrics**: Orders per minute by zone, drift detection events
- **Performance Metrics**: Processing latency, message throughput
- **System Health**: Consumer uptime, Kafka message rates
- **ADWIN Algorithm**: Rolling means and concept drift detection

## Quick Start

### 1. Start the Monitoring Stack

```bash
# Start Prometheus and Grafana
./setup_monitoring.sh
```

This script will:
- Start Prometheus (port 9090) and Grafana (port 3000)
- Launch a metrics test script to generate sample data
- Verify all components are working correctly

### 2. Access the Dashboards

- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Metrics Endpoint**: http://localhost:8000/metrics

The SurgeOpt dashboard will be automatically provisioned in Grafana.

## Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────┐
│   SurgeOpt      │    │  Prometheus  │    │   Grafana   │
│   Consumer      │───▶│  (Scraper)   │───▶│ (Visualizer)│
│   + Metrics     │    │              │    │             │
└─────────────────┘    └──────────────┘    └─────────────┘
         │                       │
         │                       ▼
         ▼               ┌──────────────┐
┌─────────────────┐      │  Alerting    │
│ HTTP Server     │      │  Rules       │
│ :8000/metrics   │      │              │
└─────────────────┘      └──────────────┘
```

## Metrics Reference

### Business Metrics

| Metric | Type | Description | Labels |
|--------|------|-------------|--------|
| `surgeopt_orders_per_minute` | Gauge | Current orders per minute | `zone` |
| `surgeopt_orders_processed_total` | Counter | Total processed orders | `zone`, `status` |
| `surgeopt_adwin_drift_detected_total` | Counter | ADWIN drift detections | `zone` |

### Performance Metrics

| Metric | Type | Description | Labels |
|--------|------|-------------|--------|
| `surgeopt_consumer_processing_seconds` | Histogram | Message processing time | - |
| `surgeopt_kafka_messages_total` | Counter | Kafka message count | `topic`, `status` |
| `surgeopt_consumer_uptime_seconds` | Gauge | Consumer uptime | - |

### ADWIN Algorithm Metrics

| Metric | Type | Description | Labels |
|--------|------|-------------|--------|
| `surgeopt_adwin_rolling_mean` | Gauge | Current ADWIN rolling mean | `zone` |

## Dashboard Panels

### 1. Orders Per Minute by Zone
- **Type**: Time series
- **Query**: `surgeopt_orders_per_minute`
- **Purpose**: Track real-time order volume across different zones

### 2. Total Order Processing Rate
- **Type**: Gauge
- **Query**: `sum(rate(surgeopt_orders_processed_total[5m])) * 60`
- **Purpose**: Monitor overall system throughput

### 3. Processing Latency
- **Type**: Time series
- **Queries**: 
  - `histogram_quantile(0.95, rate(surgeopt_consumer_processing_seconds_bucket[5m]))`
  - `histogram_quantile(0.50, rate(surgeopt_consumer_processing_seconds_bucket[5m]))`
- **Purpose**: Track 50th and 95th percentile latency

### 4. ADWIN Rolling Mean by Zone
- **Type**: Time series
- **Query**: `surgeopt_adwin_rolling_mean`
- **Purpose**: Monitor ADWIN algorithm state

### 5. Drift Detection Events
- **Type**: Time series (bars)
- **Query**: `increase(surgeopt_adwin_drift_detected_total[5m])`
- **Purpose**: Visualize concept drift detection events

### 6. Consumer Uptime
- **Type**: Gauge
- **Query**: `surgeopt_consumer_uptime_seconds`
- **Purpose**: Monitor system health

### 7. Kafka Message Rate
- **Type**: Time series
- **Query**: `rate(surgeopt_kafka_messages_total[5m])`
- **Purpose**: Monitor message throughput by topic and status

## Alerting Rules

### Critical Alerts

1. **DriftDetected**: Fires immediately when concept drift is detected
2. **ConsumerDown**: Fires if consumer is unreachable for 30+ seconds

### Warning Alerts

1. **HighOrderVolume**: Orders per minute > 50 for 2+ minutes
2. **HighProcessingLatency**: 95th percentile > 0.5s for 1+ minute
3. **LowOrderProcessingRate**: Processing rate < 5 orders/min for 2+ minutes

## Integration with SurgeOpt Consumer

The monitoring is integrated into the SurgeOpt consumer through the `SurgeOptMetrics` class:

```python
from src.metrics.exporter import get_metrics

# Get metrics instance (singleton)
metrics = get_metrics()

# Start HTTP server for Prometheus scraping
metrics.start_server(port=8000)

# Record metrics in your code
metrics.update_orders_per_minute(zone, orders_count)
metrics.record_drift_detection(zone)
metrics.record_processing_time(duration)
```

### Key Integration Points

1. **Message Processing**: Record processing time and success/failure
2. **ADWIN Algorithm**: Update rolling means and drift detection events
3. **Order Processing**: Track orders per minute and processing success
4. **System Health**: Monitor uptime and Kafka message rates

## Configuration Files

### Prometheus Configuration
- **File**: `infra/prometheus.yml`
- **Scrape Interval**: 10 seconds for SurgeOpt metrics
- **Retention**: 200 hours

### Grafana Provisioning
- **Datasources**: `infra/grafana/provisioning/datasources/prometheus.yml`
- **Dashboards**: `infra/grafana/provisioning/dashboards/dashboard.yml`
- **Dashboard JSON**: `infra/grafana/dashboards/surgeopt-dashboard.json`

### Docker Compose
- **Prometheus**: Port 9090, mounted config files
- **Grafana**: Port 3000, provisioned datasources and dashboards

## Development and Testing

### Running Tests

```bash
# Run metrics tests
python -m pytest tests/test_metrics.py -v

# Test metrics endpoint manually
python quick_metrics_test.py
```

### Adding New Metrics

1. Add metric definition to `src/metrics/exporter.py`
2. Record metric values in relevant consumer code
3. Update dashboard queries if needed
4. Add alerting rules if appropriate

### Example: Adding a New Counter

```python
# In SurgeOptMetrics.__init__()
self.my_new_counter = Counter(
    'surgeopt_my_new_metric_total',
    'Description of my metric',
    ['label1', 'label2']
)

# In your consumer code
metrics.my_new_counter.labels(label1='value1', label2='value2').inc()
```

## Troubleshooting

### Common Issues

1. **Metrics not appearing in Prometheus**
   - Check if metrics server is running: `curl http://localhost:8000/metrics`
   - Verify Prometheus configuration and restart if needed

2. **Grafana dashboard empty**
   - Ensure Prometheus datasource is configured correctly
   - Check that metrics are available in Prometheus UI

3. **Alerts not firing**
   - Verify alerting rules syntax in Prometheus UI
   - Check that metrics values meet alert conditions

### Useful Commands

```bash
# Check container status
docker compose ps

# View Prometheus logs
docker compose logs prometheus

# View Grafana logs
docker compose logs grafana

# Test metrics endpoint
curl http://localhost:8000/metrics | grep surgeopt

# Query Prometheus API
curl "http://localhost:9090/api/v1/query?query=surgeopt_orders_per_minute"
```

## Production Considerations

1. **Security**: Configure authentication for Grafana and Prometheus
2. **Storage**: Set up persistent volumes for metrics retention
3. **Alerting**: Configure Alertmanager for notification routing
4. **High Availability**: Consider running multiple Prometheus instances
5. **Resource Limits**: Set appropriate CPU and memory limits for containers

## References

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Python Prometheus Client](https://github.com/prometheus/client_python)
