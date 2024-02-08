# Проектная работа 6 спринта

### [link to git](https://github.com/KseniiaKarpova/Async_API_sprint_3)
# Запуск проекта
### 1 step
create **.env** file based on **.env.example**<br>
```bash
cp env_example .env
```
Edit .env file.
### 2 step
Сборка проекта
```bash
docker-compose up -d --build
```

### 3 step
Провести миграции для postgres_file_api сервиса
docker-compose run file_api alembic revision --autogenerate -m "{название миграции}"
docker-compose run file_api alembic upgrade "{название миграции}"

### 4 step
Заполнение базы данных из sqlite в Postgres

```bash
curl -XGET http://0.0.0.0:8888/migrate
```

### 5 step
Посмотреть результат загрузки данных через Админку
```bash
curl -XGET http://127.0.0.1:80/api/v1/movies/
```

### 6 step

Пример:
```bash
curl -X 'GET' \
  'http://127.0.0.1:8080/api/v1/persons/6dd77305-18ee-4d2e-9215-fd1a496ccfdf/film' \
  -H 'accept: application/json'
```
# Links

1.[Django admin panel](http://127.0.0.1:80/admin/)  
2.[Swagger для FastApi](http://127.0.0.1:8080/api/openapi)  
3.[Minio S3](http://localhost:9001)  
4.[Swagger для  FileApi](http://localhost:2080/api/openapi)  


# Tests
```bash
docker-compose -f docker-compose-tests.yml up --build
```

unit-тесты для сервиса FileAPI:
```bash
docker exec file_api pytest /app/test.py
```