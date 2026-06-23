EcomFlow

BigData платформа аналитики e-commerce в реальном времени.
Стек: Kafka, ZooKeeper, Spark, PostgreSQL, MongoDB, FastAPI, Docker.

GitHub Actions: passing


О проекте

EcomFlow — учебная BigData платформа которая принимает события
интернет-магазина (просмотры, клики, заказы) в реальном времени,
обрабатывает их через Apache Kafka и Apache Spark, хранит в
PostgreSQL и MongoDB, и отображает аналитику на живом дашборде.


Стек технологий

Слой             Технологии
-----------      --------------------------------------------------
Стриминг         Apache Kafka 3.5, ZooKeeper
Batch обработка  Apache Spark 3.5 (PySpark)
Хранение         PostgreSQL 16, MongoDB 7
API              FastAPI (Python 3.12)
Фронтенд         HTML, CSS, JavaScript, Chart.js
Инфраструктура   Docker, Docker Compose
CI/CD            GitHub Actions


Архитектура

    Генератор событий (Python Producer)
               |
        Apache Kafka
        (топик: ecom.user-events)
          /              \
    Kafka Consumer     Apache Spark
    (Python)           (PySpark batch job)
          \              /
       PostgreSQL     MongoDB
       (заказы)       (каталог)
               |
        FastAPI (REST API)
               |
        Dashboard (HTML/CSS/JS)


Что умеет платформа

    - принимает события в реальном времени через Kafka
    - генерирует случайные события (view, click, purchase)
    - считает дневную выручку и топ товаров через PySpark
    - хранит заказы и транзакции в PostgreSQL
    - хранит каталог товаров в MongoDB
    - отдаёт аналитику через REST API
    - отображает живой дашборд с графиками


Быстрый старт

Требования:
    Docker Desktop 4.x+
    WSL2 (для Windows)
    Python 3.12+
    Java 21+ (для Spark)
    8+ ГБ RAM

Установка:

    git clone https://github.com/imash1999/ecomflow.git
    cd ecomflow
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

Запуск инфраструктуры:

    docker-compose up -d

Запуск producer (генератор событий):

    python3 services/producer/producer.py

Запуск consumer (читает из Kafka):

    python3 services/producer/consumer.py

Запуск Spark batch job:

    export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
    python3 services/spark/batch_revenue.py

Запуск API:

    uvicorn services.api.main:app --host 0.0.0.0 --port 8000 --reload


Веб-интерфейсы

    Kafka UI     http://localhost:8080
    API Docs     http://localhost:8000/docs
    Dashboard    http://localhost:8000/dashboard


API эндпоинты

    GET /                         статус сервиса
    GET /api/users                список пользователей
    GET /api/orders               список заказов
    GET /api/revenue              статистика выручки
    GET /api/products             каталог товаров
    GET /api/products/{id}        один товар


Подключение к базам данных

    PostgreSQL:
    docker exec -it ecomflow-postgres psql -U ecom_user -d ecomflow

    MongoDB:
    docker exec -it ecomflow-mongodb mongosh \
      "mongodb://ecom_user:ecom_pass@localhost:27017/ecomflow?authSource=admin"


Структура проекта

    ecomflow/
    ├── .github/
    │   └── workflows/
    │       └── ci.yml              GitHub Actions CI
    ├── scripts/
    │   ├── init_postgres.sql       инициализация PostgreSQL
    │   └── init_mongo.js           инициализация MongoDB
    ├── services/
    │   ├── api/
    │   │   └── main.py             FastAPI приложение
    │   ├── producer/
    │   │   ├── producer.py         Kafka producer
    │   │   └── consumer.py         Kafka consumer
    │   ├── spark/
    │   │   └── batch_revenue.py    PySpark batch job
    │   └── dashboard/
    │       └── index.html          веб-дашборд
    ├── docker-compose.yml
    ├── requirements.txt
    └── README.md


Автор

    Iman — https://github.com/imash1999
