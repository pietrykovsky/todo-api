FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /api/requirements.txt
COPY ./api /api
WORKDIR /api

RUN pip install -r requirements.txt && \
    adduser --disabled-password --no-create-home django-user && \
    chown -R django-user:django-user /api && \
    chmod -R 755 /api

USER django-user