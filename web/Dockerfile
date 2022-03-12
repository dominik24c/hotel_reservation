FROM python:3.10.2-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt update && python -m pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

