import math
import os.path as op
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

import orjson
from mashumaro.mixins.orjson import DataClassORJSONMixin

from .api import API_UP_VIDEO
from .consts import DIR_SAMPLE
from .login import session
from .rest import loads_rest
from .utils import write_sample
from .wbi import wbi_sign_params


@dataclass
class Video:
    # comment: int
    # typeid: int
    # play: int
    # pic: str
    # subtitle: str
    # description: str
    # copyright: str
    # title: str
    # review: int
    # author: str
    mid: int
    # created: int
    # length: str
    # video_review: int
    aid: int
    bvid: str
    # hide_click: bool
    # is_pay: int
    # is_union_video: int
    # is_steins_gate: int
    # is_live_playback: int
    # is_lesson_video: int
    # is_lesson_finished: int
    # lesson_update_info: str
    # jump_url: str
    # meta: dict | None
    # is_avoided: int
    # season_id: int
    # attribute: int
    # is_charging_arc: bool
    # vt: int
    # enable_vt: int
    # vt_display: str
    # playback_position: int


@dataclass
class Page:
    pn: int
    ps: int
    count: int


@dataclass
class List:
    # 此处不能使用 tuple
    # tuple 不可变，会丢失数据
    vlist: list[Video]


@dataclass
class Arc(DataClassORJSONMixin):
    list: List
    page: Page


class OrderEnum(Enum):
    pubdate = 'pubdate'
    click = 'click'
    stow = 'stow'


def gen_params(
    mid: str,
    order: str = OrderEnum.pubdate.value,
    keyword: str = '',
    pn: int = 1,
    ps: int = 30,
) -> dict[str, str | int]:
    return dict(
        mid=mid,
        order=order,
        tid=0,
        keyword=keyword,
        pn=pn,
        ps=ps,
    )


session.headers.update(
    {
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
        'referer': 'https://www.bilibili.com/',
    }
)


def query_all_video(mid: str) -> Iterable[Video]:
    def inner(params):
        res = session.get(API_UP_VIDEO, params=wbi_sign_params(params))
        write_sample(res.content)
        rest = loads_rest(res.content, Arc)
        data = rest.data
        return data

    init_data = inner(gen_params(mid))
    page = init_data.page
    all_page = math.ceil(page.count / page.ps)
    yield from init_data.list.vlist
    sys.stdout.write(f'\r[page] 1/{all_page}')

    for i in range(all_page - 1):
        yield from inner(gen_params(mid, pn=i + 2)).list.vlist
        sys.stdout.write(f'\r[page] {i+2}/{all_page}')
    print()


def dump_all_video(mid: str):
    filename = f'video_of_{mid}.json'
    filepath = op.join(DIR_SAMPLE, filename)
    vlist = query_all_video(mid)
    with open(filepath, 'wb') as fp:
        fp.write(orjson.dumps(vlist))
