from fake_useragent import FakeUserAgent
from requests import Session

__all__ = ['new_session']


def new_session():
    session = Session()
    session.headers.update(
        {
            'user-agent': FakeUserAgent().random,
            # 'referer': 'https://www.bilibili.com/',
        }
    )
    return session
