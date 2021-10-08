import asyncio
import logging

from core.queue import queue
from core.logging import configure_logging

configure_logging()


async def main():
    logging.info("Initializing Kimberly worker..")
    queue.consume()

asyncio.run(main())
