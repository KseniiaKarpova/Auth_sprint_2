FROM python:3.10

ENV TZ=Europe/Moscow

WORKDIR /src

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY . /src