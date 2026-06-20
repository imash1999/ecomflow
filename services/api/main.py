from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import psycopg2.extras
from pymongo import MongoClient
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="EcomFlow API", version="1.0.0")

# CORS — чтобы фронтенд мог обращаться к API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение к PostgreSQL
def get_pg():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="ecomflow",
        user="ecom_user",
        password="ecom_pass"
    )

# Подключение к MongoDB
mongo = MongoClient("mongodb://ecom_user:ecom_pass@localhost:27017/ecomflow?authSource=admin")
db_mongo = mongo["ecomflow"]


# ─── Эндпоинты ───────────────────────────

@app.get("/")
def root():
    return {"status": "ok", "project": "EcomFlow"}


@app.get("/api/users")
def get_users():
    """Все пользователи из PostgreSQL"""
    conn = get_pg()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM users ORDER BY created_at DESC")
    users = cur.fetchall()
    conn.close()
    return {"users": list(users)}


@app.get("/api/orders")
def get_orders():
    """Все заказы из PostgreSQL"""
    conn = get_pg()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT o.id, o.total, o.status, o.created_at, u.name as user_name
        FROM orders o
        JOIN users u ON o.user_id = u.id
        ORDER BY o.created_at DESC
    """)
    orders = cur.fetchall()
    conn.close()
    return {"orders": list(orders)}


@app.get("/api/revenue")
def get_revenue():
    """Общая выручка и статистика"""
    conn = get_pg()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT
            COUNT(*)                            as total_orders,
            SUM(total)                          as total_revenue,
            AVG(total)                          as avg_order,
            COUNT(*) FILTER (WHERE status='completed') as completed
        FROM orders
    """)
    stats = cur.fetchone()
    conn.close()
    return {"stats": dict(stats)}


@app.get("/api/products")
def get_products():
    """Каталог товаров из MongoDB"""
    products = list(db_mongo.products.find({}, {"_id": 1, "name": 1, "price": 1, "stock": 1, "rating": 1}))
    for p in products:
        p["id"] = p.pop("_id")
    return {"products": products}


@app.get("/api/products/{product_id}")
def get_product(product_id: str):
    """Один товар из MongoDB"""
    product = db_mongo.products.find_one({"_id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product["id"] = product.pop("_id")
    return {"product": product}
# Раздача дашборда
app.mount("/static", StaticFiles(directory="services/dashboard"), name="static")

@app.get("/dashboard")
def dashboard():
    return FileResponse("services/dashboard/index.html")
