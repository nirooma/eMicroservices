import asyncio

from core.queue import queue


async def main():
    print("worker kimberly is running.")
    queue.consume()

asyncio.run(main())
