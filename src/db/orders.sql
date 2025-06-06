-- src/db/orders.sql

CREATE TABLE IF NOT EXISTS orders (
    order_id UUID PRIMARY KEY,
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    timestamp TIMESTAMP NOT NULL
);
