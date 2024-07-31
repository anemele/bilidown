import json
import logging
import os.path as op
import time
from dataclasses import asdict, dataclass
from hashlib import md5
from typing import Any
from urllib.parse import urlencode

from bilidown.utils import one_day

from .api import API_NAV
from .consts import DIR_CACHE
from .request import new_session
from .rest import loads_rest
from .tools import write_sample

logger = logging.getLogger(__file__)


@dataclass
class WBI_IMG:
    img_url: str
    sub_url: str


# @dataclass
class NAV:
    def __init__(self, wbi_img, **kw) -> None:
        self.wbi_img = WBI_IMG(**wbi_img)  # type: ignore


@dataclass
class WBI_Key:
    img_key: str
    sub_key: str
    expire: float


FILE_WBI_KEY = op.join(DIR_CACHE, 'wbi_key.json')


def get_wbi_keys() -> WBI_Key:
    if op.exists(FILE_WBI_KEY):
        with open(FILE_WBI_KEY, 'rb') as fp:
            keys: WBI_Key = json.load(fp, object_hook=lambda obj: WBI_Key(**obj))
        logger.debug(keys)
        if keys.expire > time.time():
            return keys

    res = new_session().get(API_NAV)
    write_sample(res.content)

    rest = loads_rest(res.content, NAV)
    data: NAV = rest.data
    wbi = data.wbi_img
    logger.debug(wbi)

    keys = WBI_Key(
        wbi.img_url.rsplit('/', 1)[-1].split('.', 1)[0],
        wbi.sub_url.rsplit('/', 1)[-1].split('.', 1)[0],
        one_day(),
    )
    with open(FILE_WBI_KEY, 'w') as fp:
        json.dump(asdict(keys), fp)

    return keys


# fmt: off
MixinKeyEncTab = (
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52
)
# fmt: on


def get_mixin_key(orig: str) -> str:
    return ''.join(orig[i] for i in MixinKeyEncTab)[:32]


def enc_wbi(params: dict[str, Any], img_key: str, sub_key: str) -> dict[str, Any]:
    # 过滤 value 中的 !'()* 字符
    filter_table = {ord(c): '' for c in "!'()*"}
    params = {k: str(v).translate(filter_table) for k, v in params.items()}

    params['wts'] = round(time.time())  # 添加 wts 字段
    params = dict(sorted(params.items()))  # 按照 key 重排参数。 Python3.6+ 字典带有顺序

    query = urlencode(params)  # 序列化参数
    mixin_key = get_mixin_key(img_key + sub_key)
    wbi_sign = md5((query + mixin_key).encode()).hexdigest()  # 计算 w_rid
    params['w_rid'] = wbi_sign

    return params


def wbi_sign_params(params: dict[str, Any]) -> dict[str, Any]:
    keys = get_wbi_keys()
    return enc_wbi(
        params=params,
        img_key=keys.img_key,
        sub_key=keys.sub_key,
    )
