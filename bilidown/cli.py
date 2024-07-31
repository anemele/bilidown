from .query import dump_all_video


def query_video():
    try:
        print('------------------------')
        print('bilidown@anemele')
        print('type in `mid` to download all video info of a bilibili UP')
        print('leave empty to exit')
        print('------------------------')
        while x := input('mid: '):
            dump_all_video(x)
    except KeyboardInterrupt:
        pass
