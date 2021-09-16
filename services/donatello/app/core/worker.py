import os
import time

from celery import Celery


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("RABBITMQ_URL", "amqp://localhost:5672")
celery.conf.result_backend = os.environ.get("REDIS_URL", "redis://localhost:6379")
celery.conf.timezone = os.getenv("DEFAULT_TIMEZONE", "Asia/Jerusalem")
