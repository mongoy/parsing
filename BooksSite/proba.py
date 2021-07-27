import aiohttp
import asyncio


HOST = 'https://www.labirint.ru'

URL = 'https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table'

HEADERS = {
    'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.114 YaBrowser/21.6.1.274 Yowser/2.5 Safari/537.36",
    'Accept': '*/*',
}


async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get(url=URL) as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html[:15], "...")

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

asyncio.run(main())
