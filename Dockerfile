FROM python:3.11-slim-buster
LABEL authors="lyapin"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip  \
    && pip install --no-cache-dir -r ./requirements.txt

COPY . .