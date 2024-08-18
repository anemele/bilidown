import os.path as op
import time
from dataclasses import dataclass
from enum import IntEnum

import orjson
from mashumaro.mixins.orjson import DataClassORJSONMixin
from qrcode import make
from requests.utils import dict_from_cookiejar

from .api import API_QR_GEN, API_QR_POLL
from .consts import DIR_CACHE
from .log import logger
from .request import new_session
from .rest import loads_rest
from .utils import write_sample

session = new_session()


@dataclass
class QRInfo(DataClassORJSONMixin):
    url: str
    qrcode_key: str


def get_qrcode_key():
    res = session.get(API_QR_GEN)
    write_sample(res.content)

    rest = loads_rest(res.content, QRInfo)
    data: QRInfo = rest.data
    url = data.url
    qrcode_key = data.qrcode_key

    qrimg = make(url)
    qrimg.show()

    return qrcode_key


@dataclass
class QRPoll(DataClassORJSONMixin):
    url: str
    refresh_token: str
    timestamp: int
    code: int
    message: str


class QRPollCode(IntEnum):
    succ = 0  # 扫码登录成功
    invalid = 86038  # 二维码已失效
    weiqueren = 86090  # 二维码已扫码未确认
    weisaoma = 86101  # 未扫码


def get_cookies():
    qrcode_key = get_qrcode_key()  # 180 秒有效期
    params = dict(qrcode_key=qrcode_key)

    while True:
        res = session.get(API_QR_POLL, params=params)
        write_sample(res.content)

        rest = loads_rest(res.content, QRPoll)
        data = rest.data
        logger.info(data.message)

        if data.code == QRPollCode.succ or data.code == QRPollCode.invalid:
            break

        time.sleep(2)

    return dict_from_cookiejar(session.cookies)


FILE_COOKIES = op.join(DIR_CACHE, 'cookies.json')

if op.exists(FILE_COOKIES):
    with open(FILE_COOKIES, 'rb') as fp:
        content = fp.read()
    cookies = orjson.loads(content)
    session.cookies.update(cookies)
else:
    cookies = get_cookies()
    with open(FILE_COOKIES, 'wb') as fp:
        fp.write(orjson.dumps(cookies))
