# 📈 SurgeOpt Project Plan

## 🚀 Overview

**SurgeOpt** is a real-time bonus optimization engine designed for courier platforms (e.g., Wolt, Foodora). Its core function is to detect demand-supply mismatches, forecast short-term courier demand, and recommend €/km surge bonuses per zone.

The system ingests real-time order events, identifies demand spikes using online learning (ADWIN), forecasts near-future demand using LightGBM, and solves an optimization problem using PuLP to determine zone-based surges. Results are exposed via API and communicated to internal stakeholders via Slack alerts.

---

## 🎯 Project Goals

- ✅ Ingest real-time courier order and supply events.
- ✅ Detect sudden demand spikes using ADWIN.
- ✅ Forecast future demand using LightGBM.
- ✅ Compute optimal €/km bonuses using PuLP/CBC.
- ✅ Serve surge results via REST API.
- ✅ Push alerts to Slack for human-in-the-loop validation.
- ✅ Expose system metrics via Prometheus + Grafana.

---

## 🗓️ 8-Week Development Timeline

| Week | Milestone                                                                 |
|------|--------------------------------------------------------------------------|
| 1    | 🐳 **Docker Compose Setup**: Kafka, Postgres, Prometheus, Kafdrop        |
| 2    | 🔁 **Simulate.py**: Mock `order_created` events into Kafka               |
| 3    | 🧠 **ADWIN Spike Detector** + Postgres persistence                       |
| 4    | 📈 **LightGBM Trainer** + Forecasting service                            |
| 5    | 💶 **PuLP Optimizer** for €/km matrix                                    |
| 6    | 🌐 **FastAPI Endpoint + Slack Alerts + LLM Summary (opt.)**              |
| 7    | 📊 **Prometheus Metrics + Grafana Dashboards**                           |
| 8    | 🧪 **Replay Mode**, documentation polish, blog post, and code freeze     |

---

## 🔧 Architecture Overview

### Data Flow Diagram (Textual)

```
simulate.py → Kafka [order_created] → consumer.py → Postgres
↓
ADWIN Spike Detection
↓
Kafka [gap_detected] → optimizer
↓
PuLP/CBC → €/km surge matrix → FastAPI
↓
Slack + JSON API + Prometheus
```

---

## 📦 Tech Stack

| Layer         | Technology                 |
|---------------|----------------------------|
| Language      | Python 3.12                |
| Ingestion     | Apache Kafka (Docker)      |
| Stream UI     | Kafdrop                    |
| DB            | PostgreSQL                 |
| Spike Detect  | River (ADWIN)              |
| Forecasting   | LightGBM                   |
| Optimizer     | PuLP + CBC solver          |
| API           | FastAPI (REST)             |
| Messaging     | Slack (incoming webhook)   |
| Observability | Prometheus + Grafana       |
| CI/CD         | GitHub Actions             |
| Docs          | MkDocs                     |
| Versioning    | Git (Conventional Commits) |

---

## ✅ Completed (End of Week 2)

- [x] Kafka + Zookeeper running in Docker
- [x] Kafdrop available at http://localhost:9000
- [x] PostgreSQL container ready (`surgeopt` DB)
- [x] Kafka producer (`simulate.py`) sending mock `order_created` messages
- [x] Kafka consumer receiving and printing those messages
- [ ] (Postgres insert logic pending)
- [ ] (Prometheus unconfigured but available)

---

## 🔜 Next Steps

### Week 3 Tasks

- [ ] Create `orders.sql` schema
- [ ] Insert Kafka orders into Postgres
- [ ] Count orders/minute and integrate ADWIN
- [ ] Publish spike events to Kafka topic `gap_detected`
- [ ] Add Prometheus metric: `orders_per_minute`

---

## 📁 Folder Structure (Proposed)

```
surgeopt/
├── src/
│   ├── simulator/
│   │   └── simulate.py
│   ├── consumer/
│   │   └── consumer.py
│   ├── adwin/
│   │   └── detector.py
│   ├── optimizer/
│   │   └── optimizer.py
│   ├── api/
│   │   └── main.py
│   ├── db/
│   │   └── orders.sql
│   └── metrics/
│       └── exporter.py
├── docker-compose.yml
├── PROJECT_PLAN.md
├── README.md
└── docs/
    └── index.md
```

---

## 📐 Development Standards

- Follow **PEP8** for all Python code.
- Use **type hints** and **docstrings** in all modules.
- Use **Conventional Commits** (e.g., `feat:`, `fix:`, `chore:`).
- Add GitHub Issues for every task and assign them.
- Use **feature branches** for all work. One feature = one PR.
- All merges require at least one review.

---

## 🚦 CI/CD

We will implement the following stages in GitHub Actions:

1. `lint` – run `flake8` or `ruff`
2. `test` – run unit tests (if available)
3. `docker` – build & optionally push Docker image
4. `docs` – deploy `MkDocs` to GitHub Pages

---

## 🧠 Why This Architecture?

- **Kafka**: Decouples event ingestion from processing (can scale independently).
- **Postgres**: Stores historical orders for both forecasting and auditing.
- **River (ADWIN)**: Lightweight real-time anomaly detection suited for streaming.
- **LightGBM**: Fast gradient boosting for demand forecasting.
- **PuLP/CBC**: Easy to formulate and solve constrained optimization models.
- **FastAPI**: Production-grade async API with automatic docs.
- **Prometheus/Grafana**: Standard stack for observability in real-time systems.

---

## 🧪 Replay Mode (Week 8)

We'll add a `replay.py` script to:

- Ingest a historical CSV of order events
- Replay them in accelerated time through Kafka
- Allow system validation over 24h of real data in 10 minutes

---

## 📝 Documentation Plan

- `/docs/index.md`: Project intro, setup, and architecture
- `/docs/dev-notes.md`: Developer onboarding, Git flow, coding guidelines
- `/docs/modules/*.md`: Spike detection, forecasting, optimizer, API
- `/docs/observability.md`: Prometheus metrics, Grafana dashboards
- `/docs/blog/*.md`: Engineering deep dives (for open-source credibility)

---

## ✨ Stretch Goals

- [ ] Add gRPC support alongside REST (FastAPI)
- [ ] Add Slack bot for manual zone override
- [ ] Persist forecasts & surge prices to DB
- [ ] Add Docker health checks & liveness probes

---

## 🧑‍💻 Core Contributors

| Name      | Role     | GitHub                  |
|-----------|----------|--------------------------|
| Daniel    | Tech Lead / Project Manager | [@djelacik](https://github.com/djelacik) |
| Kartik    | Developer                   | [@kpatel](https://github.com/KartikPat250905)  |

---

> Print this plan. Read it when lost. Stick to the system — and the system will scale.