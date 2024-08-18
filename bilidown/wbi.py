import os.path as op
import time
from dataclasses import dataclass
from hashlib import md5
from typing import Any
from urllib.parse import urlencode

from mashumaro.mixins.orjson import DataClassORJSONMixin

from .api import API_NAV
from .log import logger
from .path import FILE_WBI_KEY
from .request import new_session
from .rest import loads_rest
from .utils import one_day, write_sample


@dataclass
class WBI_IMG:
    img_url: str
    sub_url: str


@dataclass
class NAV(DataClassORJSONMixin):
    wbi_img: WBI_IMG


@dataclass
class WBI_Key(DataClassORJSONMixin):
    img_key: str
    sub_key: str
    expire: float


def get_wbi_keys() -> WBI_Key:
    if op.exists(FILE_WBI_KEY):
        with open(FILE_WBI_KEY, 'rb') as fp:
            content = fp.read()
        keys = WBI_Key.from_json(content)
        logger.debug(keys)
        if keys.expire > time.time():
            return keys

    res = new_session().get(API_NAV)
    write_sample(res.content)

    rest = loads_rest(res.content, NAV)
    data = rest.data
    wbi = data.wbi_img
    logger.debug(wbi)

    keys = WBI_Key(
        img_key=wbi.img_url.rsplit('/', 1)[-1].split('.', 1)[0],
        sub_key=wbi.sub_url.rsplit('/', 1)[-1].split('.', 1)[0],
        expire=one_day(),
    )
    with open(FILE_WBI_KEY, 'wb') as fp:
        fp.write(keys.to_jsonb())

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
