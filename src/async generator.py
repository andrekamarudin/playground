import asyncio
import time
from typing import AsyncGenerator


async def slow_task(i: int) -> str:
    await asyncio.sleep(0.1)  # simulate work
    return f"Task {i} done"


# Sequential: tasks run one after another
async def sequential_gen(n: int) -> AsyncGenerator[str, None]:
    for i in range(n):
        result = await slow_task(i)
        yield result


# Concurrent: all tasks start at once, yield as they complete
async def concurrent_gen(n: int) -> AsyncGenerator[str, None]:
    tasks = [slow_task(i) for i in range(n)]
    for task in asyncio.as_completed(tasks):
        result = await task
        yield result


async def main():
    n = 50

    # Sequential: ~5 seconds (50 * 0.1s)
    start = time.perf_counter()
    async for _ in sequential_gen(n):
        pass
    sequential_time = time.perf_counter() - start

    # Concurrent: ~0.1 second (all tasks run in parallel)
    start = time.perf_counter()
    async for _ in concurrent_gen(n):
        pass
    concurrent_time = time.perf_counter() - start

    print(f"Sequential: {sequential_time:.2f}s")
    print(f"Concurrent: {concurrent_time:.2f}s")
    print(f"Speedup: {sequential_time / concurrent_time:.1f}x")


if __name__ == "__main__":
    asyncio.run(main())
