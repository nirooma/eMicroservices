import asyncio
import logging

from app.core.queue import queue
from app.core.logging import configure_logging

configure_logging()


async def main():
    logging.info("Initializing Kimberly worker..")
    queue.consume()

asyncio.run(main())
