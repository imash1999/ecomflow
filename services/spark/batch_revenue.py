from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, count, avg, col, to_date

# ─── Подключение к Spark ───────────────
spark = SparkSession.builder \
    .appName("EcomFlow - Daily Revenue") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

PG_URL  = "jdbc:postgresql://localhost:5432/ecomflow"
PG_PROPS = {
    "user":     "ecom_user",
    "password": "ecom_pass",
    "driver":   "org.postgresql.Driver"
}

print("Loading data from PostgreSQL...")

# ─── Читаем данные ─────────────────────
orders = spark.read.jdbc(PG_URL, "orders", properties=PG_PROPS)
items  = spark.read.jdbc(PG_URL, "order_items", properties=PG_PROPS)

orders.createOrReplaceTempView("orders")
items.createOrReplaceTempView("order_items")

print(f"Orders loaded: {orders.count()}")
print(f"Items loaded:  {items.count()}")

# ─── Аналитика по дням ─────────────────
daily = spark.sql("""
    SELECT
        to_date(created_at) as date,
        COUNT(*)            as orders_cnt,
        SUM(total)          as revenue,
        AVG(total)          as avg_order
    FROM orders
    WHERE status = 'completed'
    GROUP BY to_date(created_at)
    ORDER BY date DESC
""")

print("\nDaily Revenue Report:")
daily.show()

# ─── Топ товаров ───────────────────────
top_products = spark.sql("""
    SELECT
        product_id,
        name,
        SUM(quantity)       as total_sold,
        SUM(price*quantity) as total_revenue
    FROM order_items
    GROUP BY product_id, name
    ORDER BY total_revenue DESC
""")

print("Top Products:")
top_products.show()

# ─── Сохраняем агрегаты в PostgreSQL ───
print("Writing results to daily_revenue table...")

daily.select("date", "revenue", "orders_cnt") \
    .write \
    .jdbc(
        PG_URL,
        "daily_revenue",
        mode="append",
        properties=PG_PROPS
    )

print("Done! Results saved to PostgreSQL.")
spark.stop()
