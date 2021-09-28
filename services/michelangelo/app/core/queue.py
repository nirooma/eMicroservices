import datetime
import time
from typing import List, Tuple

from kombu import Connection, Exchange, Queue

from app.core.config import settings
import logging

from app.core.configuration_utils import config


logger = logging.getLogger(__name__)


class QueueBaseHandler:
    EXCHANGE_NAME = "donatello"
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
        ("notifications", "notifications.*")
    ]

    def __init__(self):
        self.connection = Connection(settings.RABBITMQ_URL)
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
                    name=queue[0],
                    exchange=self.exchange,
                    routing_key=queue[1]
                )
                for queue in self.queue_list
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
        self._disconnect()

    def set_consumer(self, consumption_queue: Tuple[str, str]):
        """
        consumption_queue > ("queue_name", "routing_key")
        """
        if self._consumer is None:
            queue = Queue(
                name=consumption_queue[0],
                routing_key=consumption_queue[1],
                exchange=self.exchange
            )
            if consumption_queue[0] not in self.queue_list:
                self.queues.append(queue)
            self._consumer = self.connection.Consumer(queues=queue)
        return self._consumer

    def consume(self):
        self._connect()
        self._consumer.register_callback(callback)
        if not self._consumer:
            raise Exception("Run 'set_consumer' method first. ")
        with self._consumer:
            print("Waiting for a new messages...")
            while True:
                try:
                    self.connection.drain_events(timeout=1)
                except Exception as e:
                    pass


def callback(body, message):
    queue_message = queue_callback_message_format(body, message)
    print(queue_message)
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
    queue.prepare_data(task_name, task_details=task_details, routing_key=routing_key)
    queue.publish()
    logger.info(f"task was send to the queue. {task_details=}")
