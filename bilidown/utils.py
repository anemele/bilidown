import os
import os.path as op
import time


def mkdir(path: str, gitignore: bool = False):
    if not op.exists(path):
        os.mkdir(path)
    if gitignore:
        with open(op.join(path, '.gitignore'), 'w') as fp:
            fp.write('*')


def one_day():
    return time.time() + 86400
