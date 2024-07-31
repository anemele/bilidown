from enum import Enum

from .api import API_UP_VIDEO
from .login import session
from .tools import write_sample
from .wbi import wbi_sign_params


class OrderEnum(Enum):
    pubdate = 'pubdate'
    click = 'click'
    stow = 'stow'


query_params = dict(
    mid=2,
    order=OrderEnum.pubdate.value,
    tid=0,
    keyword='',
    pn=1,
    ps=30,
)

session.headers.update(
    {
        'referer': 'www.bilibili.com',
    }
)
res = session.get(API_UP_VIDEO, params=wbi_sign_params(query_params))
write_sample(res.content)
