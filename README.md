EcomFlow

Платформа аналитики e-commerce в реальном времени на базе BigData-стека.


Стек технологий

Слой           Технологии
-----------    --------------------------------------------------
Стриминг       Apache Kafka, ZooKeeper
Обработка      Apache Spark, Apache Flink
Хранение       PostgreSQL, MongoDB, Cassandra, HBase
Аналитика      Hadoop, Hive
API            FastAPI (Python), Spring Boot (Java)
Фронтенд       HTML, CSS, JavaScript
Инфраструктура Docker, Kubernetes, Linux
CI/CD          GitHub Actions


Быстрый старт

Требования:
- Docker Desktop 4.x+
- WSL2 (для Windows)
- 8+ ГБ RAM

Запуск:

    git clone https://github.com/YOUR_USERNAME/ecomflow.git
    cd ecomflow
    cp .env.example .env
    docker-compose up -d

Веб-интерфейсы:

    Kafka UI    http://localhost:8080
    API Docs    http://localhost:8000/docs
    Dashboard   http://localhost:8000/dashboard


Архитектура

    Источники данных (Web, Orders, Catalog)
               |
        REST API (FastAPI)
               |
        Apache Kafka + ZooKeeper
          /              \
    Apache Flink      Apache Spark
    (real-time)       (batch)
          \              /
      Cassandra  PostgreSQL  MongoDB
               |
        Query API (FastAPI)
               |
        Dashboard (HTML/CSS/JS)


Структура проекта

    ecomflow/
    ├── services/
    │   ├── api/           FastAPI REST endpoints
    │   ├── producer/      Kafka producer
    │   └── dashboard/     HTML/CSS/JS фронтенд
    ├── scripts/
    │   ├── init_postgres.sql
    │   └── init_mongo.js
    ├── docker-compose.yml
    └── .env.example


Подключение к БД

    PostgreSQL:
    psql -h localhost -U ecom_user -d ecomflow

    MongoDB:
    mongosh "mongodb://ecom_user:ecom_pass@localhost:27017/ecomflow?authSource=admin"
