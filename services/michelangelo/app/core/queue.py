import datetime
import time
from typing import List, Tuple

from kombu import Connection, Exchange, Queue

from app.core.config import settings
import logging

from app.core.configuration_utils import config


logger = logging.getLogger(__name__)


class QueueBaseHandler:
    EXCHANGE_NAME = "eMicroservices"
    EXCHANGE_TYPE = "topic"

    __slots__ = [
        "queues_list",
        "connection",
        "exchange_name",
        "routing_key",
        "exchange_type",
        "_queues",
        "_exchange",
        "_producer",
        "_consumer",
        "still_consumed"
    ]

    retry_policy = {
        "interval_start": 0,
        "interval_step": 2,
        "interval_max": 30,
        "max_retries": 30
    }

    queue_list: List[Tuple[str, str]] = [
        ("notifications", "notifications.*"),
        ("authentication", "authentication.*")
    ]

    def __init__(self, connection: str = None):
        self.connection = Connection(connection or settings.RABBITMQ_URL)
        self._queues = None
        self._producer = None
        self._exchange = None
        self._consumer = None

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.connection.hostname})>"

    @property
    def producer(self):
        if self._producer is None:
            self._producer = self.connection.Producer()
        return self._producer

    @property
    def exchange(self):
        if self._exchange is None:
            self._exchange = Exchange(name=self.EXCHANGE_NAME, type=self.EXCHANGE_TYPE)
        return self._exchange

    @property
    def queues(self):
        if self._queues is None:
            return [
                Queue(
                    name=queue_[0],
                    exchange=self.exchange,
                    routing_key=queue_[1]
                )
                for queue_ in self.queue_list
            ]
        return self._queues

    @classmethod
    def prepare_data(cls, task_name: str, *, task_details: dict, routing_key: str):
        """ Must be called every time for a different message """
        cls.data = {
            "body": {
                "task": task_name,
                "timestamp": datetime.datetime.now(),
                "details": {
                    **task_details
                }
            },
            "properties": {
                "routing_key": routing_key
            }
        }

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

    def publish(self):
        self._connect()
        self.producer.publish(
            body=self.data["body"],
            routing_key=self.data["properties"]["routing_key"],
            exchange=self.exchange,
            retry=True,
            retry_policy=self.retry_policy,
            declare=self.queues
        )
        logger.info(f"Michelangelo worker published to queue {self.data['properties']['routing_key']!r}")
        self._disconnect()

    def _set_consumer(self):
        queue_name, routing_key = config.get("my_queue_name"), config.get("my_routing_key")
        if self._consumer is None:
            queue_ = Queue(
                name=queue_name,
                routing_key=routing_key,
                exchange=self.exchange
            )
            if queue_name not in self.queue_list:
                self.queues.append(queue_)
            self._consumer = self.connection.Consumer(queues=queue_)

        logger.info(f"Michelangelo worker is listening to queue {queue_name!r}")
        return self._consumer

    def consume(self):
        self._connect()
        self._set_consumer()
        self._consumer.register_callback(callback)
        if not self._consumer:
            raise Exception("Run 'set_consumer' method first. ")

        logging.info("Michelangelo worker is running, ready to accept connections.")
        with self._consumer:
            while True:
                try:
                    self.connection.drain_events(timeout=1)
                except Exception as e:
                    pass

                time.sleep(2)


def callback(body, message):
    queue_message = queue_callback_message_format(body, message)
    prefix, task_name = queue_message["task"].split(".")

    logger.info(f"Getting message from the queue, {prefix=}, {task_name=}")
    logger.debug(f"Message details {queue_message=}")
    message.ack()


def queue_callback_message_format(body, message):
    return {
        "properties": {
            "timestamp": datetime.datetime.now(),
            "exchange": message.delivery_info.get("exchange"),
            "routing_key": message.delivery_info.get("routing_key")
        },
        "task": body["task"],
        "details": body["details"],
        "send_to_queue_timestamp": body["timestamp"]
    }


queue = QueueBaseHandler()


def send_task_to_queue(task_name: str, task_details: dict, routing_key: str = config.get("gRouting_key")):
    queue_ = QueueBaseHandler()
    queue_.prepare_data(task_name, task_details=task_details, routing_key=routing_key)
    queue_.publish()
