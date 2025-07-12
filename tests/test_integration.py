"""
Tests for the integrated async demo.
"""

import asyncio

import httpx
import pytest
from src.integrated_async_demo import (
    concurrent_http_gen,
    fetch_url,
    sequential_http_gen,
)


class TestAsyncIntegration:
    @pytest.mark.asyncio
    async def test_fetch_url_success(self):
        """Test successful URL fetch."""
        async with httpx.AsyncClient() as client:
            result = await fetch_url(client, "https://httpbin.org/status/200")

            assert result["success"] is True
            assert result["status"] == 200
            assert result["url"] == "https://httpbin.org/status/200"

    @pytest.mark.asyncio
    async def test_sequential_generator(self):
        """Test sequential HTTP generator."""
        urls = ["https://httpbin.org/status/200", "https://httpbin.org/status/201"]

        async with httpx.AsyncClient() as client:
            results = []
            async for result in sequential_http_gen(client, urls):
                results.append(result)

            assert len(results) == 2
            assert all(r["success"] for r in results)

    @pytest.mark.asyncio
    async def test_concurrent_generator(self):
        """Test concurrent HTTP generator."""
        urls = ["https://httpbin.org/status/200", "https://httpbin.org/status/201"]

        async with httpx.AsyncClient() as client:
            results = []
            async for result in concurrent_http_gen(client, urls):
                results.append(result)

            assert len(results) == 2
            assert all(r["success"] for r in results)


if __name__ == "__main__":
    # Simple test runner for when pytest is not available
    async def run_tests():
        test_instance = TestAsyncIntegration()

        print("🧪 Running basic tests...")

        try:
            await test_instance.test_fetch_url_success()
            print("✅ test_fetch_url_success passed")
        except Exception as e:
            print(f"❌ test_fetch_url_success failed: {e}")

        try:
            await test_instance.test_sequential_generator()
            print("✅ test_sequential_generator passed")
        except Exception as e:
            print(f"❌ test_sequential_generator failed: {e}")

        try:
            await test_instance.test_concurrent_generator()
            print("✅ test_concurrent_generator passed")
        except Exception as e:
            print(f"❌ test_concurrent_generator failed: {e}")

    asyncio.run(run_tests())
