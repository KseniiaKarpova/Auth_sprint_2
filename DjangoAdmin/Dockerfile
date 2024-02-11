FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240


ENV TZ=Europe/Moscow

USER root

RUN apt-get update && apt-get install -y gettext

COPY run_uwsgi.sh /app/run_uwsgi.sh
COPY requirements.txt requirements.txt
COPY uwsgi/uwsgi.ini uwsgi.ini

RUN  mkdir -p /var/www/static/ \
     && mkdir -p /var/www/media/ \
     && mkdir -p /app/static/ \
     && mkdir -p /app/media/ \
     && pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir


COPY . /app
ENV DJANGO_SETTINGS_MODULE 'config.settings'

ENTRYPOINT [ "sh", "/app/run_uwsgi.sh" ]