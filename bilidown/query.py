from enum import Enum

from .api import API_UP_VIDEO
from .login import session
from .tools import write_sample
from .wbi import wbi_sign_params

session.headers.update(
    {
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
        'referer': 'https://www.bilibili.com/',
    }
)


class OrderEnum(Enum):
    pubdate = 'pubdate'
    click = 'click'
    stow = 'stow'


query_params = dict(
    mid=-1,
    order=OrderEnum.pubdate.value,
    tid=0,
    keyword='',
    pn=2,
    ps=30,
)

res = session.get(API_UP_VIDEO, params=wbi_sign_params(query_params))
write_sample(res.content)
