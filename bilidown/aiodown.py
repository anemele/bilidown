import asyncio

import aiofiles
import aiohttp
from fake_useragent import FakeUserAgent


async def download_video(bvid: str, path: str):
    async with aiohttp.ClientSession() as session:
        session.headers.update(
            {
                'user-agent': FakeUserAgent().random,
                'referer': 'https://www.bilibili.com/',
            }
        )

        url = bvid
        async with session.get(url) as res:
            content = await res.read()

    async with aiofiles.open(path, 'wb') as fp:
        await fp.write(content)
