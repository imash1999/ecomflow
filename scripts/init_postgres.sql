CREATE TABLE IF NOT EXISTS users (
    id         SERIAL PRIMARY KEY,
    email      VARCHAR(255) UNIQUE NOT NULL,
    name       VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS orders (
    id         SERIAL PRIMARY KEY,
    user_id    INTEGER REFERENCES users(id),
    total      DECIMAL(10,2) NOT NULL,
    status     VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS order_items (
    id         SERIAL PRIMARY KEY,
    order_id   INTEGER REFERENCES orders(id),
    product_id VARCHAR(100) NOT NULL,
    name       VARCHAR(255) NOT NULL,
    price      DECIMAL(10,2) NOT NULL,
    quantity   INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS daily_revenue (
    date       DATE PRIMARY KEY,
    revenue    DECIMAL(12,2),
    orders_cnt INTEGER,
    updated_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO users (email, name) VALUES
    ('alice@example.com', 'Alice Smith'),
    ('bob@example.com',   'Bob Johnson'),
    ('carol@example.com', 'Carol White')
ON CONFLICT DO NOTHING;

INSERT INTO orders (user_id, total, status) VALUES
    (1, 1250.00, 'completed'),
    (2, 340.50,  'completed'),
    (1, 89.99,   'pending'),
    (3, 2100.00, 'completed')
ON CONFLICT DO NOTHING;

INSERT INTO order_items (order_id, product_id, name, price, quantity) VALUES
    (1, 'prod-001', 'Laptop Stand', 250.00, 5),
    (1, 'prod-002', 'USB Hub',      100.00, 10),
    (2, 'prod-003', 'Mouse',         34.05, 10),
    (3, 'prod-004', 'Keyboard',      89.99, 1),
    (4, 'prod-005', 'Monitor 27"',  700.00, 3)
ON CONFLICT DO NOTHING;

CREATE INDEX IF NOT EXISTS idx_orders_user_id    ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at);
