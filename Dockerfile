FROM python:3.10-slim

RUN apt-get update

RUN apt-get install -y git

ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry

ENV PATH="/usr/local/bin:${PATH}"

COPY . .

RUN poetry install