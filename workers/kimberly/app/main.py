import asyncio
from core.config import config
from core.queue import queue
import os


async def main():
    queue.consume()

asyncio.run(main())
