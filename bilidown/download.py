from dataclasses import dataclass

from .api import API_VIDEO_PLAYURL, API_VIDEO_VIEW
from .login import session
from .rest import loads_rest
from .tools import write_sample
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


# 下载视频需要请求头标明 ua 和 referer
session.headers.update({'referer': 'https://www.bilibili.com/'})


def download_video(bvid: str):
    # 参数可以用 avid 和 bvid ，推荐 bvid
    res = session.get(API_VIDEO_VIEW, params=wbi_sign_params(dict(bvid=bvid)))
    write_sample(res.content)
    data: View = loads_rest(res.content, View).data
    cid = data.cid

    res = session.get(
        API_VIDEO_PLAYURL, params=wbi_sign_params(dict(bvid=bvid, cid=cid))
    )
    write_sample(res.content)
    playurl: PlayURL = loads_rest(res.content, PlayURL).data

    for i, seg in enumerate(playurl.durl):
        with open(f'{bvid}_{i:02d}.mp4', 'wb') as fp:
            fp.write(session.get(seg.url.replace(r'\u0026', '&')).content)
