FROM python:3.10.2-slim-buster

ENV APP_DIR=/app
RUN mkdir $APP_DIR
RUN mkdir $APP_DIR/static

WORKDIR $APP_DIR

COPY requirements.txt .

RUN apt update && python -m pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

