#!/bin/bash
# stop_system.sh - Stop the entire SurgeOpt monitoring system

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${RED}🛑 Stopping SurgeOpt System${NC}"
echo "=============================="

# Stop metrics server
echo -e "\n${YELLOW}Stopping Metrics Server...${NC}"
if [ -f scripts/.metrics_pid ]; then
    PID=$(cat scripts/.metrics_pid)
    if kill $PID 2>/dev/null; then
        echo -e "✅ Stopped metrics server (PID: $PID)"
    else
        echo -e "⚠️  Metrics server already stopped"
    fi
    rm scripts/.metrics_pid
else
    # Try to find and kill any running metrics process
    if pkill -f "start_metrics.py" 2>/dev/null; then
        echo -e "✅ Stopped metrics server"
    else
        echo -e "⚠️  No metrics server running"
    fi
fi

# Stop consumer if running
echo -e "\n${YELLOW}Stopping Consumer...${NC}"
if pkill -f "src.consumer.consumer" 2>/dev/null; then
    echo -e "✅ Stopped consumer"
else
    echo -e "⚠️  No consumer running"
fi

# Stop producer if running
echo -e "\n${YELLOW}Stopping Producer...${NC}"
if pkill -f "src.simulator.producer" 2>/dev/null; then
    echo -e "✅ Stopped producer"
else
    echo -e "⚠️  No producer running"
fi

# Stop Docker services
echo -e "\n${YELLOW}Stopping Docker Services...${NC}"
docker compose down

echo -e "\n${GREEN}✅ System Stopped Successfully!${NC}"
echo "================================"
echo -e "\n📝 ${YELLOW}What was stopped:${NC}"
echo "  • Metrics server"
echo "  • Consumer (if running)"
echo "  • Producer (if running)"
echo "  • Prometheus"
echo "  • Grafana"
echo "  • Kafka"
echo "  • PostgreSQL"

echo -e "\n🚀 ${YELLOW}To restart:${NC}"
echo -e "  ${BLUE}./complete_startup.sh${NC}"
