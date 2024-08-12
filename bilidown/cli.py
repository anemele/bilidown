import os.path as op
import sys
import time

from .aiodown import download_all_video as _a_download_all_video
from .aiodown import download_video as _a_download_video
from .consts import DIR_SAMPLE
from .download import download_video as _download_video
from .query import dump_all_video as _dump_all_video
from .query import query_all_video as _query_all_video
from .utils import mkdir


def query_video():
    try:
        print('------------------------')
        print('bilidown@anemele')
        print('type in `mid` to download all video info of a bilibili UP')
        print('leave empty to exit')
        print('------------------------')
        while x := input('mid: '):
            try:
                _dump_all_video(x)
            except Exception as e:
                print(e)
    except KeyboardInterrupt:
        pass


def download_video():
    try:
        print('------------------------')
        print('bilidown@anemele')
        print('type in `bvid` to download the video')
        print('leave empty to exit')
        print('------------------------')
        while x := input('bvid: '):
            try:
                _a_download_video(x)
            except Exception as e:
                print(e)
    except KeyboardInterrupt:
        pass


def download_all_video():
    try:
        print('------------------------')
        print('bilidown@anemele')
        print('type in `mid` to download all videos of a bilibili UP')
        print('leave empty to exit')
        print('------------------------')
        while x := input('mid: '):
            # try:
            #     vs = _query_all_video(x)
            # except Exception as e:
            #     print(e)
            #     continue

            # path = op.join(DIR_SAMPLE, x)
            # mkdir(path)
            # for i, v in enumerate(vs, 1):
            #     try:
            #         _download_video(v.bvid, path)
            #         sys.stdout.write(f'\rdone {i}')
            #         time.sleep(2)  # 反爬？异步？
            #     except Exception as e:
            #         print(e)
            #         continue
            # print()
            _a_download_all_video(x)
    except KeyboardInterrupt:
        pass
