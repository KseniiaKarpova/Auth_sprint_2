FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

COPY . /app

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8888"]