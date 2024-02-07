# Tests

### Запуск:
```bash
docker-compose -f docker-compose-tests.yml up --build

docker exec test_auth_api alembic upgrade head 

docker run tests
```