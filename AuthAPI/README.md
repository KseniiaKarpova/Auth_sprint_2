## Работа с миграциями Alembic

### Если в alembic/versions есть файл с миграцией а в бд их нет то применить их:
```bash
alembic upgrade head
```  
### Откатить миграции из бд к началу
```bash
alembic downgrade base
```

###  Откатить миграции из бд на один шаг 
```bash
alembic downgrade -1
```

### Если изменен файл с описанием таблиц, то создать миграцию
```bash
alembic revision --autogenerate -m 'Name of migration(changed some field or created user table)'
```

# Создание Супер Пользователя:
```bash
 docker exec AuthAPI python cli_create_super_user.py [login] [password]
```
