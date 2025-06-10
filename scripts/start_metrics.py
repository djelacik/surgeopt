#!/usr/bin/env python3
"""
start_metrics.py - Start the SurgeOpt metrics server with sample data

This script:
1. Starts the Prometheus metrics HTTP server
2. Generates realistic sample data to demonstrate the monitoring system
3. Keeps running to provide data for Prometheus and Grafana
"""

import sys
import os
import time
import random
import signal
import requests

# Add the parent directory to the Python path so we can import from src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.metrics.exporter import get_metrics

class MetricsDemo:
    def __init__(self):
        self.running = True
        self.metrics = get_metrics()
        self.zones = ["Kallio", "Kamppi", "Punavuori", "Kruununhaka", "Töölö"]
        self.counter = 0
        
        # Handle Ctrl+C gracefully
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    def start(self):
        """Start the metrics server and data generation"""
        print("🚀 Starting SurgeOpt Metrics Server...")
        
        # Start the HTTP server
        self.metrics.start_server(port=8000)
        print("📊 Metrics server started at http://localhost:8000/metrics")
        
        # Wait a moment for server to start
        time.sleep(2)
        
        # Verify server is working
        import requests
        try:
            response = requests.get("http://localhost:8000/metrics", timeout=5)
            if response.status_code == 200:
                print("✅ Metrics server is responding correctly")
            else:
                print(f"❌ Metrics server returned status {response.status_code}")
                return
        except Exception as e:
            print(f"❌ Failed to connect to metrics server: {e}")
            return
        
        print("📝 Generating sample metrics data...")
        print("📈 You can now check:")
        print("   • Metrics: http://localhost:8000/metrics")
        print("   • Prometheus: http://localhost:9090")
        print("   • Grafana: http://localhost:3000 (admin/admin)")
        print("\n🔄 Press Ctrl+C to stop")
        
        # Generate realistic data
        self.generate_data()
    
    def generate_data(self):
        """Generate realistic metrics data for demonstration"""
        while self.running:
            self.counter += 1
            
            try:
                # Generate realistic order data for each zone
                for zone in self.zones:
                    # Simulate different patterns for different zones
                    if zone == "Kamppi":  # Busy downtown area
                        base_orders = 35
                        variation = 15
                    elif zone == "Kallio":  # Trendy area with variable demand
                        base_orders = 25
                        variation = 20
                    elif zone == "Punavuori":  # Business district
                        base_orders = 30
                        variation = 10
                    else:  # Other areas
                        base_orders = 20
                        variation = 12
                    
                    # Add time-based patterns (rush hours, etc.)
                    hour_of_day = (self.counter // 6) % 24
                    if 11 <= hour_of_day <= 13 or 17 <= hour_of_day <= 19:  # Lunch and dinner rush
                        rush_multiplier = 1.5
                    elif 6 <= hour_of_day <= 10:  # Morning
                        rush_multiplier = 1.2
                    else:  # Off-peak
                        rush_multiplier = 0.8
                    
                    # Calculate orders per minute with some randomness
                    orders_per_min = int((base_orders + random.randint(-variation, variation)) * rush_multiplier)
                    orders_per_min = max(5, orders_per_min)  # Minimum 5 orders
                    
                    # Update business metrics
                    self.metrics.update_orders_per_minute(zone, orders_per_min)
                    self.metrics.update_adwin_mean(zone, orders_per_min * 0.95)  # Slightly lower than current
                    
                    # Simulate order processing
                    for _ in range(random.randint(1, 3)):  # Process 1-3 orders per cycle
                        success = random.random() > 0.05  # 95% success rate
                        self.metrics.record_order_processed(zone, success=success)
                    
                    # Occasionally simulate drift detection
                    if random.random() < 0.02:  # 2% chance per zone per cycle
                        self.metrics.record_drift_detection(zone)
                        print(f"🚨 Simulated concept drift detected in {zone}")
                
                # Simulate system performance metrics
                processing_time = 0.05 + random.expovariate(10)  # Exponential distribution
                processing_time = min(processing_time, 2.0)  # Cap at 2 seconds
                self.metrics.record_processing_time(processing_time)
                
                # Simulate Kafka messages
                topics = ["order_created", "order_updated", "order_completed"]
                for topic in topics:
                    if random.random() < 0.8:  # 80% chance of message per topic
                        success = random.random() > 0.02  # 98% success rate
                        timeout = random.random() < 0.01 if not success else False  # 1% timeout rate
                        self.metrics.record_kafka_message(topic, success=success, timeout=timeout)
                
                # Update uptime
                self.metrics.update_uptime()
                
                # Progress indicator
                if self.counter % 10 == 0:
                    print(f"📊 Generated {self.counter} data points... (Ctrl+C to stop)")
                
                # Wait before next iteration
                time.sleep(10)  # Generate data every 10 seconds
                
            except Exception as e:
                print(f"❌ Error generating metrics: {e}")
                time.sleep(5)
        
        print("👋 Metrics generation stopped")

def main():
    demo = MetricsDemo()
    demo.start()

if __name__ == "__main__":
    main()
