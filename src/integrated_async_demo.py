import asyncio
import time
from typing import AsyncGenerator

import httpx


async def fetch_url(client: httpx.AsyncClient, url: str, delay: float = 0) -> dict:
    """Fetch a single URL with optional delay to simulate varying response times."""
    if delay:
        await asyncio.sleep(delay)

    try:
        response = await client.get(url, timeout=10.0)
        return {
            "url": url,
            "status": response.status_code,
            "length": len(response.text),
            "success": True,
        }
    except Exception as e:
        return {
            "url": url,
            "status": None,
            "length": 0,
            "success": False,
            "error": str(e),
        }


# Sequential HTTP requests: one after another
async def sequential_http_gen(
    client: httpx.AsyncClient, urls: list[str]
) -> AsyncGenerator[dict, None]:
    """Generate HTTP responses sequentially - each request waits for the previous one."""
    for i, url in enumerate(urls):
        # Add some artificial delay to simulate varying response times
        delay = 0.1 * (i % 3)  # 0, 0.1, 0.2 second delays
        result = await fetch_url(client, url, delay)
        yield result


# Concurrent HTTP requests: all start at once, yield as they complete
async def concurrent_http_gen(
    client: httpx.AsyncClient, urls: list[str]
) -> AsyncGenerator[dict, None]:
    """Generate HTTP responses concurrently - all requests start immediately."""
    tasks = []
    for i, url in enumerate(urls):
        # Add some artificial delay to simulate varying response times
        delay = 0.1 * (i % 3)  # 0, 0.1, 0.2 second delays
        task = fetch_url(client, url, delay)
        tasks.append(task)

    # Yield results as they complete (not necessarily in order)
    for task in asyncio.as_completed(tasks):
        result = await task
        yield result


# Batch processing: process URLs in batches to limit concurrent connections
async def batch_http_gen(
    client: httpx.AsyncClient, urls: list[str], batch_size: int = 5
) -> AsyncGenerator[dict, None]:
    """Process URLs in batches to control concurrency."""
    for i in range(0, len(urls), batch_size):
        batch = urls[i : i + batch_size]
        tasks = [fetch_url(client, url, 0.05) for url in batch]

        # Process batch concurrently
        for task in asyncio.as_completed(tasks):
            result = await task
            yield result


async def demonstrate_patterns():
    """Demonstrate different async patterns with HTTP requests."""

    # Test URLs - mix of real and mock URLs for demonstration
    urls = [
        "https://httpbin.org/delay/0",
        "https://httpbin.org/status/200",
        "https://httpbin.org/json",
        "https://httpbin.org/uuid",
        "https://httpbin.org/base64/SFRUUEJJTiBpcyBhd2Vzb21l",
        "https://httpbin.org/status/201",
        "https://httpbin.org/headers",
        "https://httpbin.org/ip",
    ]

    async with httpx.AsyncClient() as client:
        print("🚀 Async HTTP Request Patterns Demo\n")

        # Sequential pattern
        print("📋 Sequential Pattern (one at a time):")
        start = time.perf_counter()
        results = []
        async for result in sequential_http_gen(client, urls):
            results.append(result)
            status = "✅" if result["success"] else "❌"
            print(
                f"  {status} {result['url']} -> {result['status']} ({result['length']} bytes)"
            )

        sequential_time = time.perf_counter() - start
        print(f"⏱️  Sequential time: {sequential_time:.2f}s\n")

        # Concurrent pattern
        print("⚡ Concurrent Pattern (all at once):")
        start = time.perf_counter()
        results = []
        async for result in concurrent_http_gen(client, urls):
            results.append(result)
            status = "✅" if result["success"] else "❌"
            print(
                f"  {status} {result['url']} -> {result['status']} ({result['length']} bytes)"
            )

        concurrent_time = time.perf_counter() - start
        print(f"⏱️  Concurrent time: {concurrent_time:.2f}s\n")

        # Batch pattern
        print("📦 Batch Pattern (controlled concurrency):")
        start = time.perf_counter()
        results = []
        async for result in batch_http_gen(client, urls, batch_size=3):
            results.append(result)
            status = "✅" if result["success"] else "❌"
            print(
                f"  {status} {result['url']} -> {result['status']} ({result['length']} bytes)"
            )

        batch_time = time.perf_counter() - start
        print(f"⏱️  Batch time: {batch_time:.2f}s\n")

        # Summary
        print("📊 Performance Summary:")
        print(f"  Sequential: {sequential_time:.2f}s")
        print(f"  Concurrent: {concurrent_time:.2f}s")
        print(f"  Batch:      {batch_time:.2f}s")
        if sequential_time > 0:
            print(f"  Speedup (concurrent): {sequential_time / concurrent_time:.1f}x")
            print(f"  Speedup (batch):      {sequential_time / batch_time:.1f}x")


async def simple_generator_demo():
    """Simple demonstration from the original async generator example."""
    print("\n🔄 Simple Async Generator Demo\n")

    async def count_async(n: int) -> AsyncGenerator[str, None]:
        for i in range(n):
            await asyncio.sleep(0.1)  # Simulate some async work
            yield f"Count: {i + 1}"

    print("Counting asynchronously:")
    async for item in count_async(5):
        print(f"  {item}")


async def main():
    """Main entry point demonstrating integrated async patterns."""
    try:
        await demonstrate_patterns()
        await simple_generator_demo()
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("🎯 Integrated Async Demo - Generators + HTTP Requests")
    print("=" * 60)
    asyncio.run(main())
