from bilidown import query_all_video

if __name__ == "__main__":
    while True:
        uid = input("up uid: ")
        if not uid:
            break
        if not uid.isdigit():
            print("uid must be a number")
            continue
        for video in query_all_video(uid):
            print(video.bvid, video.title)
