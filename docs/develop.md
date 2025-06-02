# Developer Guide

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/djelacik/surgeopt.git
cd surgeopt
```

### 2. Start services
```bash
docker-compose up --build
```

Includes: Kafka, Kafdrop, Postgres, Prometheus, Grafana

## Project Structure

```
surgeopt/
├── src/               ← Python services
├── docker/            ← Container configs
├── notebooks/         ← Forecast exploration
├── tests/             ← pytest test suite
├── docs/              ← MkDocs site
├── .github/workflows/ ← CI/CD pipelines
└── mkdocs.yml
```

## CI/CD

GitHub Actions runs:
- `ruff`, `black`, `mypy` for code style
- `pytest` for tests
- `mkdocs gh-deploy` to publish docs