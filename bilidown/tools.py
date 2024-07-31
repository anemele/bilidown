import os.path as op

from .consts import DIR_SAMPLE
from .utils import get_timestamp


def write_sample(content: bytes):
    return
    filename = f'{get_timestamp()}.json'
    filepath = op.join(DIR_SAMPLE, filename)
    with open(filepath, 'wb') as fp:
        fp.write(content)
