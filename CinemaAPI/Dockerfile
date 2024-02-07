FROM python:3.10

ENV TZ=Europe/Moscow

WORKDIR /app

COPY requirements.txt .
RUN apt-get update

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY . /app