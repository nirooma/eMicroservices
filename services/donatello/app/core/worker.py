import os

from celery import Celery

from app.core.config import settings

celery = Celery(__name__)
celery.conf.broker_url = settings.RABBITMQ_URL
celery.conf.result_backend = settings.REDIS_URL
celery.conf.timezone = settings.DEFAULT_TIMEZONE
