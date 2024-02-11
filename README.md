# Проектная работа 7 спринта
### [link to git](https://github.com/KseniiaKarpova/Auth_sprint_2)

## Техническое задание:
1. Создайте интеграцию Auth-сервиса с сервисом выдачи контента и панелью администратора Django, используя контракт, который вы сделали в прошлом задании.
  
    При создании интеграции не забудьте учесть изящную деградацию Auth-сервиса. Как вы уже выяснили ранее, Auth сервис один из самых нагруженных, потому что в него ходят большинство сервисов сайта. И если он откажет, сайт отказать не должен. Обязательно учтите этот сценарий в интеграциях с Auth-сервисом.
2. Добавьте в Auth трасировку и подключите к Jaeger. Для этого вам нужно добавить работу с заголовком x-request-id и отправку трасировок в Jaeger.
3. Добавьте в сервис механизм ограничения количества запросов к серверу.
4. Партицируйте таблицу с пользователями. 
Подумайте, по каким критериям вы бы разделили её. Важно посмотреть на таблицу не только в текущем времени, но и заглядывая в некое будущее, когда в ней будут миллионы записей. Пользователи могут быть из одной страны, но из разных регионов. А ещё пользователи могут использовать разные устройства для входа и иметь разные возрастные ограничения.
5. Упростите регистрацию и аутентификацию пользователей в Auth-сервисе, добавив вход через социальные сервисы. Список сервисов выбирайте исходя из целевой аудитории онлайн-кинотеатра — подумайте, какими социальными сервисами они пользуются. Например, использовать [OAuth от Github](https://docs.github.com/en/free-pro-team@latest/developers/apps/authorizing-oauth-apps) — не самая удачная идея. Ваши пользователи не разработчики и вряд ли имеют аккаунт на Github. А вот добавить VK, Google, Yandex или Mail будет хорошей идеей.

    Вам не нужно делать фронтенд в этой задаче и реализовывать собственный сервер OAuth. Нужно реализовать протокол со стороны потребителя.
    
    Информация по OAuth у разных поставщиков данных: 
    
    - [Yandex](https://yandex.ru/dev/oauth/?turbo=true),
    - [VK](https://vk.com/dev/access_token),
    - [Google](https://developers.google.com/identity/protocols/oauth2),
    - [Mail](https://api.mail.ru/docs/guides/oauth/).
    
**Дополнительное задание**
Реализуйте возможность открепить аккаунт в соцсети от личного кабинета.


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
4.[Swagger для FileApi](http://localhost:2080/api/openapi)  
5.[Swagger для AuthAPI](http://localhost:9999/api/openapi)


# Tests
```bash
docker-compose -f docker-compose-tests.yml up --build
```

unit-тесты для сервиса FileAPI:
```bash
docker exec file_api pytest /app/test.py
```