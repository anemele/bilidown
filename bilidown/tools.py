import os.path as op
import time

from . import ENABLE_WRITE_SAMPLE
from .consts import DIR_SAMPLE


def write_sample(content: bytes):
    if not ENABLE_WRITE_SAMPLE:
        return

    filename = f'{time.time_ns()}.json'
    filepath = op.join(DIR_SAMPLE, filename)
    with open(filepath, 'wb') as fp:
        fp.write(content)
