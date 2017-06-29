linkage-worker
===============

Celery worker app for running data-linking tasks. It is used as part of Data-linking-ui to create and scale celery
worker containers with separate code base using docker-compose.

Inspired by https://github.com/itsrifat/flask-celery-docker-scale to create celery worker with separate code base.

:License: MIT


Settings
--------

The following environment variables must be specified for celery configuration:
    - CELERY_BROKER_URL : For example, redis://localhost:6379/0


Celery
^^^^^^

The data-linking web application uses Celery workers to run linking jobs asynchronously.
You need to setup a Celery broker like Redis or
RabbitMQ and start a Celery worker.

The Celery broker is provided by CELERY_BROKER_URL environment variable.


