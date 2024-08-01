import os.path as op
from dataclasses import dataclass

from .api import API_VIDEO_PLAYURL, API_VIDEO_VIEW
from .login import session
from .request import new_session
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


def download_video(bvid: str, path: str = '.'):
    # 参数可以用 avid 和 bvid ，推荐 bvid
    # 视频清晰度 qn 参考：
    # https://socialsisteryi.github.io/bilibili-API-collect/docs/video/videostream_url.html#qn%E8%A7%86%E9%A2%91%E6%B8%85%E6%99%B0%E5%BA%A6%E6%A0%87%E8%AF%86
    params = dict(bvid=bvid, qn=80)
    res = session.get(API_VIDEO_VIEW, params=wbi_sign_params(params))
    write_sample(res.content)
    data: View = loads_rest(res.content, View).data
    cid = data.cid

    res = session.get(
        API_VIDEO_PLAYURL, params=wbi_sign_params(dict(bvid=bvid, cid=cid))
    )
    write_sample(res.content)
    playurl: PlayURL = loads_rest(res.content, PlayURL).data

    # 下载多个视频后链接会断开，因此下载视频的 session 和请求数据的 session 不用同一个
    sess = new_session()
    # 下载视频需要请求头标明 ua 和 referer
    sess.headers.update({'referer': 'https://www.bilibili.com/'})
    for i, seg in enumerate(playurl.durl):
        name = f'{bvid}_{i:02d}.mp4'
        with open(op.join(path, name), 'wb') as fp:
            fp.write(sess.get(seg.url.replace(r'\u0026', '&')).content)
