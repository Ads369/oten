import aiohttp
import asyncio
import aiofiles


URL = 'http://72.en.cx/GameStat.aspx?gid=71197'
HTML_FILE = 'data/temp.html'

async def ping_main():
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            async with aiofiles.open(HTML_FILE, 'w') as out:
                await out.write(html)
                await out.flush()
            print("Body:", html[10000:10100], "...")


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ping_main())


if __name__ == '__main__':
    main()