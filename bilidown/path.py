import os.path as op

from .consts import DIR_CACHE, DIR_SAMPLE
from .utils import mkdir

mkdir(DIR_CACHE, True)
mkdir(DIR_SAMPLE, True)
FILE_WBI_KEY = op.join(DIR_CACHE, 'wbi_key.json')
