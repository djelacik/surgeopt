# Grafana Troubleshooting Guide for SurgeOpt

## What Just Happened? 🔧

You experienced a common Grafana issue: **datasource UID mismatch**. Here's exactly what was wrong and how we fixed it:

### The Problem
1. **Dashboard Expected**: Datasource UID = `prometheus`
2. **Grafana Created**: Datasource UID = `PBFA97CFB590B2093`
3. **Result**: Dashboard couldn't find the datasource → "No data"

### The Fix
```bash
# 1. Found the actual datasource UID
curl -u admin:admin "http://localhost:3000/api/datasources"

# 2. Updated dashboard to use correct UID
sed -i '' 's/"uid": "prometheus"/"uid": "PBFA97CFB590B2093"/g' grafana-import.json

# 3. Re-imported dashboard
curl -X POST -u admin:admin -d @grafana-import.json "http://localhost:3000/api/dashboards/db"
```

## How Grafana Works - Explained Simply 📊

### 1. **Data Flow**
```
Your App → Metrics Server → Prometheus → Grafana → Dashboard
    ↓           ↓              ↓          ↓         ↓
  Records    Exposes      Scrapes &   Queries   Displays
  metrics   /metrics     Stores Data    Data     Charts
```

### 2. **Key Components**

**Datasources** (Where data comes from)
- Think of it as "data connections"
- Our datasource: Prometheus at `http://prometheus:9090`
- Each datasource gets a unique ID (UID)

**Dashboards** (How data is displayed)
- Collections of panels (charts, gauges, tables)
- Each panel has queries that fetch data from datasources
- Panels reference datasources by UID

**Queries** (What data to show)
- Written in PromQL (Prometheus Query Language)
- Examples:
  - `surgeopt_orders_per_minute` - Current values
  - `rate(surgeopt_orders_processed_total[5m]) * 60` - Rate per minute

### 3. **Dashboard Panels Explained**

**Panel 1: Orders Per Minute by Zone**
- **Type**: Time series line chart
- **Query**: `surgeopt_orders_per_minute`
- **Shows**: Real-time order volume for each Helsinki zone

**Panel 2: Total Order Processing Rate**
- **Type**: Gauge (speedometer-like)
- **Query**: `sum(rate(surgeopt_orders_processed_total[5m])) * 60`
- **Shows**: Overall system throughput

**Panel 3: Processing Latency**
- **Type**: Time series with percentiles
- **Queries**: 
  - `histogram_quantile(0.95, rate(surgeopt_consumer_processing_seconds_bucket[5m]))`
  - `histogram_quantile(0.50, rate(surgeopt_consumer_processing_seconds_bucket[5m]))`
- **Shows**: How fast/slow your system is processing orders

**Panel 4: ADWIN Rolling Mean**
- **Type**: Time series
- **Query**: `surgeopt_adwin_rolling_mean`
- **Shows**: ADWIN algorithm's current state per zone

## Common Grafana Issues & Solutions 🛠️

### Issue: "No data" in panels
**Causes:**
1. ❌ Wrong datasource UID (what we just fixed)
2. ❌ Prometheus not scraping metrics
3. ❌ Metrics server not running
4. ❌ Wrong time range selected

**Debugging:**
```bash
# Check metrics server
curl http://localhost:8000/metrics

# Check Prometheus
curl "http://localhost:9090/api/v1/query?query=surgeopt_orders_per_minute"

# Check Grafana datasources
curl -u admin:admin "http://localhost:3000/api/datasources"
```

### Issue: "N/A" values
**Cause:** Usually means the query is correct but no recent data
**Solution:** Check if your metrics are being updated

### Issue: Panels loading slowly
**Cause:** Heavy queries or large time ranges
**Solution:** Reduce time range or optimize queries

## Understanding Your Current Dashboard 📈

### What You Should See Now:
1. **Orders Per Minute**: Lines showing different zones (Kallio, Kamppi, etc.)
2. **Processing Rate**: A gauge showing total orders/minute
3. **Latency**: Two lines (50th and 95th percentile response times)
4. **ADWIN Mean**: Lines showing algorithm state per zone

### How to Use the Dashboard:

**Time Controls** (Top right)
- **Last 15 minutes**: Shows recent data
- **Refresh 5s**: Auto-updates every 5 seconds
- **Time picker**: Click to change time range

**Panel Interactions**
- **Hover**: See exact values at specific times
- **Zoom**: Click and drag to zoom into time ranges
- **Legend**: Click zone names to hide/show lines

**Refresh Button**
- Force refresh if data looks stale
- Useful when troubleshooting

## Advanced Grafana Features 🚀

### 1. Creating Alerts
- Go to panel → Edit → Alert tab
- Set thresholds (e.g., orders/min > 50)
- Configure notifications (email, Slack, etc.)

### 2. Custom Queries
- Click "Edit" on any panel
- Modify PromQL queries
- Add new metrics from your application

### 3. Dashboard Variables
- Create dropdown filters (e.g., select specific zones)
- Make dashboards interactive

### 4. Annotations
- Mark important events on charts
- Useful for deployment markers, incidents

## Next Steps 🎯

1. **Explore Data**: Try different time ranges, hover over charts
2. **Learn PromQL**: Practice writing queries in Prometheus UI
3. **Customize Panels**: Edit panels to show different metrics
4. **Set Up Alerts**: Configure alerts for critical thresholds
5. **Add More Metrics**: Extend your application with additional metrics

## Quick Reference Commands 📝

```bash
# Start monitoring stack
./setup_monitoring.sh

# Check all components
curl http://localhost:8000/metrics      # Metrics server
curl http://localhost:9090/-/ready      # Prometheus health
curl http://localhost:3000/api/health   # Grafana health

# View dashboards
open http://localhost:3000              # Grafana UI (admin/admin)
open http://localhost:9090              # Prometheus UI

# Stop metrics generation
pkill -f start_metrics.py
```

Your monitoring system is now fully operational! 🎉
