import asyncio
from core.config import config
from core.queue import queue
import os


async def main():
    print("worker kimberly is running.")
    queue.consume()

asyncio.run(main())
