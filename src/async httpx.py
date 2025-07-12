import asyncio

import httpx  # no output


async def main():  # no output
    async with httpx.AsyncClient() as client:  # no output
        response = await client.get("https://example.com")  # no output
        print(response.status_code)  # 200


asyncio.run(main())  # (runs and exits after printing above)
