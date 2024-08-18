import datetime
import logging
import sys

logger = logging.getLogger(__package__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt='%(asctime)s | %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

# now = datetime.datetime.now().strftime('%Y-%m-%d')
# fn = f'{__package__} {now}.log'
# fh = logging.FileHandler(fn, encoding='utf-8')
# fh.setFormatter(formatter)
# logger.addHandler(fh)

sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(formatter)
logger.addHandler(sh)
