import asyncio
from typing import Callable, Awaitable

async def retry_async(
    func: Callable[[], Awaitable],
    retries: int = 3,
    base_delay: int = 2
):
    last_exception = None

    for attempt in range(1, retries + 1):
        try:
            return await func()
        except Exception as e:
            last_exception = e
            if attempt == retries:
                break

            await asyncio.sleep(base_delay ** attempt)

    raise last_exception
