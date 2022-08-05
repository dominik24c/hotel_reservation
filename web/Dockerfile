FROM python:3.10.2-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG APP_DIR=/app
RUN mkdir $APP_DIR
RUN mkdir $APP_DIR/static

WORKDIR $APP_DIR

RUN python -m pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 9000

