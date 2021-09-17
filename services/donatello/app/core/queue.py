import time
from typing import List, Tuple

from kombu import Connection, Exchange, Queue

from app.core.config import settings
import logging

logger = logging.getLogger("uvicorn")


class QueueBaseHandler:
    __slots__ = [
        "queues_list",
        "connection",
        "exchange_name",
        "routing_key",
        "exchange_type",
        "_queues",
        "_exchange",
        "_producer"
    ]

    retry_policy = {
        "interval_start": 0,
        "interval_step": 2,
        "interval_max": 30,
        "max_retries": 30
    }

    def __init__(self, *, queue_list: List[Tuple[str, str]], exchange_name: str, exchange_type: str):
        self.connection = Connection(settings.RABBITMQ_URL)
        self.queues_list = queue_list
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self._queues = None
        self._producer = None
        self._exchange = None

    @property
    def producer(self):
        if self._producer is None:
            self._producer = self.connection.Producer()
        return self._producer

    @property
    def exchange(self):
        if self._exchange is None:
            self._exchange = Exchange(name=self.exchange_name, type=self.exchange_type)
        return self._exchange

    @property
    def queues(self):
        if self._queues is None:
            return [
                Queue(
                    name=queue[0],
                    exchange=self.exchange,
                    routing_key=queue[1]
                )
                for queue in self.queues_list
            ]
        return self._queues

    def _connect(self):
        while not self.ping():
            try:
                self.connection.connect()
                logger.info(f"Connection established to #{self.connection.hostname}")
            except Exception as exc:
                time.sleep(5)
                logger.exception("Unable to connect to the selected queue.", exc_info=exc)

    def _disconnect(self):
        self.connection.release()

    def ping(self):
        return self.connection.connected

    def publish(self, data: dict, routing_key: str):
        self._connect()
        self.producer.publish(
            body=data,
            routing_key=routing_key,
            exchange=self.exchange,
            retry=True,
            retry_policy=self.retry_policy,
            declare=self.queues
        )
        self._disconnect()

