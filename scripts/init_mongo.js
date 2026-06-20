db = db.getSiblingDB('ecomflow');

db.products.insertMany([
  { _id: 'prod-001', name: 'Laptop Stand', category: 'accessories', price: 250.00, stock: 150, tags: ['laptop', 'ergonomic'], rating: 4.7 },
  { _id: 'prod-002', name: 'USB Hub',      category: 'accessories', price: 100.00, stock: 300, tags: ['usb', 'hub'],          rating: 4.5 },
  { _id: 'prod-003', name: 'Mouse',        category: 'peripherals', price: 34.05,  stock: 500, tags: ['mouse', 'wireless'],   rating: 4.3 },
  { _id: 'prod-004', name: 'Keyboard',     category: 'peripherals', price: 89.99,  stock: 200, tags: ['keyboard', 'rgb'],     rating: 4.8 },
  { _id: 'prod-005', name: 'Monitor 27"',  category: 'displays',    price: 700.00, stock: 75,  tags: ['monitor', '4k'],       rating: 4.6 }
]);

db.sessions.createIndex({ user_id: 1 });
db.sessions.createIndex({ created_at: 1 }, { expireAfterSeconds: 86400 });
db.events.createIndex({ user_id: 1, created_at: -1 });
db.events.createIndex({ event_type: 1 });

print('MongoDB initialized');
