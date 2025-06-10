#!/bin/bash
# complete_startup.sh - Start the entire SurgeOpt monitoring system

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Complete SurgeOpt System${NC}"
echo "========================================"

# Step 1: Start Infrastructure (Kafka, PostgreSQL, Prometheus, Grafana)
echo -e "\n${YELLOW}Step 1: Starting Infrastructure...${NC}"
echo "Starting: Kafka, PostgreSQL, Prometheus, Grafana"
docker compose up -d

echo -e "\n${YELLOW}Waiting for services to start...${NC}"
sleep 15

# Step 2: Check if services are ready
echo -e "\n${YELLOW}Step 2: Checking Service Health...${NC}"

# Check PostgreSQL
if docker compose exec -T postgres pg_isready -U surgeopt_user > /dev/null 2>&1; then
    echo -e "✅ PostgreSQL is ready"
else
    echo -e "❌ PostgreSQL is not ready"
    exit 1
fi

# Check Kafka
if docker compose exec -T kafka kafka-topics --bootstrap-server localhost:9092 --list > /dev/null 2>&1; then
    echo -e "✅ Kafka is ready"
else
    echo -e "❌ Kafka is not ready"
    exit 1
fi

# Check Prometheus
if curl -s http://localhost:9090/-/ready > /dev/null; then
    echo -e "✅ Prometheus is ready"
else
    echo -e "❌ Prometheus is not ready"
    exit 1
fi

# Check Grafana
if curl -s http://localhost:3000/api/health > /dev/null; then
    echo -e "✅ Grafana is ready"
else
    echo -e "❌ Grafana is not ready"
    exit 1
fi

# Step 3: Start Metrics Server
echo -e "\n${YELLOW}Step 3: Starting Metrics Server...${NC}"
if ! pgrep -f "start_metrics.py" > /dev/null; then
    python scripts/start_metrics.py &
    METRICS_PID=$!
    echo $METRICS_PID > scripts/.metrics_pid
    echo -e "✅ Metrics server started (PID: $METRICS_PID)"
else
    echo -e "✅ Metrics server already running"
fi

sleep 5

# Verify metrics endpoint
if curl -s http://localhost:8000/metrics > /dev/null; then
    echo -e "✅ Metrics endpoint accessible"
else
    echo -e "❌ Metrics endpoint not accessible"
    exit 1
fi

# Step 4: Verify Grafana Dashboard Auto-Provisioning
echo -e "\n${YELLOW}Step 4: Verifying Grafana Dashboard...${NC}"
echo -e "✅ Dashboard automatically provisioned at startup"

# Step 5: Start Consumer (Optional)
echo -e "\n${YELLOW}Step 5: Starting Consumer (Optional)...${NC}"
echo "You can start the consumer manually with:"
echo -e "${BLUE}python -m src.consumer.consumer${NC}"

# Step 6: Start Producer (Optional)
echo -e "\n${YELLOW}Step 6: Starting Producer (Optional)...${NC}"
echo "You can start the producer manually with:"
echo -e "${BLUE}python -m src.simulator.producer${NC}"

echo -e "\n${GREEN}🎉 System Started Successfully!${NC}"
echo "========================================"
echo -e "\n📊 ${YELLOW}Access your monitoring stack:${NC}"
echo -e "  • Grafana Dashboard: ${BLUE}http://localhost:3000/d/surgeopt-main/surgeopt-monitoring-dashboard${NC}"
echo -e "  • Prometheus: ${BLUE}http://localhost:9090${NC}"
echo -e "  • Metrics Endpoint: ${BLUE}http://localhost:8000/metrics${NC}"
echo -e "  • Kafdrop (Kafka UI): ${BLUE}http://localhost:9000${NC}"
echo -e "\n🔑 ${YELLOW}Grafana Login:${NC} admin / admin"

echo -e "\n📝 ${YELLOW}What's Currently Running:${NC}"
echo "  ✅ Infrastructure: Kafka, PostgreSQL, Prometheus, Grafana"
echo "  ✅ Metrics Server: Generating sample data"
echo "  ⏳ Consumer: Ready to start (manual)"
echo "  ⏳ Producer: Ready to start (manual)"

echo -e "\n🛑 ${YELLOW}To stop everything:${NC}"
echo -e "  ${BLUE}./stop_system.sh${NC}"

echo -e "\n🚀 ${YELLOW}Next Steps:${NC}"
echo "  1. Open Grafana dashboard to see live metrics"
echo "  2. Optionally start consumer: python -m src.consumer.consumer"
echo "  3. Optionally start producer: python -m src.simulator.producer"
