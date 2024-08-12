import asyncio
import os.path as op
from dataclasses import dataclass

import aiofiles
import aiohttp
from fake_useragent import FakeUserAgent

from .api import API_VIDEO_PLAYURL, API_VIDEO_VIEW
from .consts import DIR_SAMPLE
from .query import query_all_video
from .rest import loads_rest
from .tools import write_sample
from .utils import mkdir
from .wbi import wbi_sign_params


class View:
    def __init__(self, cid: int, **kw) -> None:
        self.cid = cid


@dataclass
class VideoSeg:
    order: int  # 	视频分段序号	某些视频会分为多个片段（从1顺序增长）
    length: int  # 	视频长度	单位为毫秒
    size: int  # 	视频大小	单位为 Byte
    ahead: str  # （？）
    vhead: str  # （？）
    url: str  # 	默认流 URL	注意 unicode 转义符    有效时间为120min
    backup_url: list[str]


class PlayURL:
    def __init__(self, durl: list[dict], **kw) -> None:
        self.durl = tuple(VideoSeg(**v) for v in durl)


async def _download_video(bvid: str, path: str):
    async with aiohttp.ClientSession() as session:
        session.headers.update(
            {
                'user-agent': FakeUserAgent().random,
                # 'referer': 'https://www.bilibili.com/',
            }
        )

        # 参数可以用 avid 和 bvid ，推荐 bvid
        # 视频清晰度 qn 参考：
        # https://socialsisteryi.github.io/bilibili-API-collect/docs/video/videostream_url.html#qn%E8%A7%86%E9%A2%91%E6%B8%85%E6%99%B0%E5%BA%A6%E6%A0%87%E8%AF%86
        params = dict(bvid=bvid, qn=80)
        async with session.get(API_VIDEO_VIEW, params=wbi_sign_params(params)) as res:
            content = await res.read()
        write_sample(content)
        data: View = loads_rest(content, View).data
        cid = data.cid

        params = dict(bvid=bvid, cid=cid)
        async with session.get(API_VIDEO_PLAYURL, params=wbi_sign_params(params)) as res:
            content = await res.read()
        write_sample(content)
        playurl: PlayURL = loads_rest(content, PlayURL).data

        session.headers.update({'referer': 'https://www.bilibili.com/'})

        for i, seg in enumerate(playurl.durl):
            name = f'{bvid}_{i:02d}.mp4'
            async with session.get(seg.url.replace(r'\u0026', '&')) as res:
                content = await res.read()
            async with aiofiles.open(op.join(path, name), 'wb') as fp:
                await fp.write(content)

            await asyncio.sleep(2)


def download_video(bvid: str, path: str = '.'):
    asyncio.run(_download_video(bvid, path))


async def _download_all_video(mid: str):
    vs = query_all_video(mid)
    root = op.join(DIR_SAMPLE, mid)
    mkdir(root)
    ret = await asyncio.gather(
        *(_download_video(v.bvid, root) for v in vs),
        return_exceptions=True,
    )
    print(f'done {len(ret)}')


def download_all_video(mid: str):
    asyncio.run(_download_all_video(mid))
