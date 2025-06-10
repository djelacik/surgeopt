# SurgeOpt
Real-time courier bonus optimiser with intelligent demand forecasting and concept drift detection.

## Overview

SurgeOpt is a comprehensive system for optimizing courier bonuses in real-time based on demand patterns across different zones. It uses advanced machine learning techniques including ADWIN (Adaptive Windowing) for concept drift detection and provides full observability through Prometheus and Grafana monitoring.

## Features

- **Real-time Order Processing**: Kafka-based message streaming for order events
- **Concept Drift Detection**: ADWIN algorithm for detecting changes in demand patterns
- **Zone-based Analytics**: Track and optimize bonuses by geographic zones
- **Comprehensive Monitoring**: Prometheus metrics and Grafana dashboards
- **Automated Alerting**: Smart alerts for drift detection and system health
- **PostgreSQL Integration**: Persistent storage for historical data

## Quick Start

### 1. Start the Infrastructure

```bash
# Start Kafka, PostgreSQL, and other dependencies
docker compose up -d kafka postgres zookeeper

# Start monitoring stack (Prometheus & Grafana)
./setup_monitoring.sh
```

### 2. Access the Monitoring Stack

- **Grafana Dashboard**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Metrics Endpoint**: http://localhost:8000/metrics

### 3. Run the Consumer

```bash
# Install dependencies
pip install -r requirements.txt

# Start the SurgeOpt consumer
python -m src.consumer.consumer
```

## Monitoring & Observability

SurgeOpt includes a comprehensive monitoring system built with Prometheus and Grafana:

### Key Metrics Tracked

- **Business KPIs**: Orders per minute by zone, processing success rates
- **Drift Detection**: ADWIN algorithm events and rolling means
- **Performance**: Processing latency percentiles, message throughput
- **System Health**: Consumer uptime, Kafka connectivity

### Dashboards

The system automatically provisions Grafana dashboards showing:
- Real-time order volumes by zone
- Concept drift detection events
- Processing latency trends
- System health indicators

### Alerting

Smart alerts are configured for:
- High order volume (>50 orders/min)
- Concept drift detection
- High processing latency (>0.5s)
- Consumer downtime
- Low processing rates

See [docs/monitoring.md](docs/monitoring.md) for detailed monitoring documentation.

## Testing

```bash
# Run all tests
python -m pytest

# Run specific test suites
python -m pytest tests/test_metrics.py -v
python -m pytest tests/test_consumer.py -v

# Test monitoring integration
python test_integration_monitoring.py
```

## Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Kafka     │    │  SurgeOpt   │    │ PostgreSQL  │
│  (Orders)   │───▶│  Consumer   │───▶│ (Storage)   │
└─────────────┘    │   + ADWIN   │    └─────────────┘
                   │   + Metrics │
                   └─────────────┘
                           │
                           ▼
                   ┌─────────────┐    ┌─────────────┐
                   │ Prometheus  │───▶│   Grafana   │
                   │ (Metrics)   │    │(Dashboards) │
                   └─────────────┘    └─────────────┘
```

## Project Structure

```
├── src/
│   ├── consumer/          # Main consumer logic
│   ├── adwin/             # ADWIN drift detection
│   ├── metrics/           # Prometheus metrics
│   ├── db/                # PostgreSQL integration
│   └── simulator/         # Order simulation
├── infra/
│   ├── prometheus.yml     # Prometheus configuration
│   └── grafana/           # Grafana dashboards & provisioning
├── tests/                 # Test suites
└── docs/                  # Documentation
```

## Development

### Environment Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Start development infrastructure
docker compose up -d

# Run tests with coverage
python -m pytest --cov=src
```

### Adding New Metrics

1. Define metrics in `src/metrics/exporter.py`
2. Record metrics in relevant consumer code
3. Update Grafana dashboards if needed
4. Add alerting rules for critical metrics

## Contributing

1. Follow [Conventional Commits](guides/conventional-commits.md)
2. Read the [Git Collaboration Guide](guides/git-collaboration-guide.md)
3. Ensure all tests pass before submitting PRs
4. Update documentation for new features

## Documentation

- [Architecture Overview](docs/architecture.md)
- [Development Guide](docs/develop.md)
- [Monitoring Setup](docs/monitoring.md)
- [Usage Examples](docs/usage.md)
- [FAQ](docs/faq.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
