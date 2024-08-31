import os
import os.path as op
import time

from .config import ENABLE_WRITE_SAMPLE
from .consts import DIR_SAMPLE


def mkdir(path: str, gitignore: bool = False):
    if not op.exists(path):
        os.mkdir(path)
    if gitignore:
        with open(op.join(path, ".gitignore"), "w") as fp:
            fp.write("*")


def one_day():
    return time.time() + 86400


def write_sample(content: bytes):
    if not ENABLE_WRITE_SAMPLE:
        return

    filename = f"{time.time_ns()}.json"
    filepath = op.join(DIR_SAMPLE, filename)
    with open(filepath, "wb") as fp:
        fp.write(content)
