# SurgeOpt Quick Start

## 🚀 **Start Everything**

```bash
# 1. Activate virtual environment (ALWAYS FORGET THIS!)
cd /Users/danieljelacik/projects/surgeopt
source venv/bin/activate

# 2. Start Docker services
docker compose up -d

# 3. Run consumer (Terminal 1)
PYTHONPATH=. python src/consumer/consumer.py

# 4. Run producer (Terminal 2) 
PYTHONPATH=. python src/simulator/producer.py
```

## 🔌 **Check Database**

```bash
# Connect to PostgreSQL
docker exec -it surgeopt-postgres-1 psql -U surgeopt -d surgeopt
```

```sql
-- Count orders
SELECT COUNT(*) FROM orders;

-- Recent orders
SELECT * FROM orders ORDER BY timestamp DESC LIMIT 5;

-- Exit
\q
```

## 🛑 **Stop Everything**

```bash
docker compose down
```