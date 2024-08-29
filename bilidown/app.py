from pathlib import Path

import orjson
from flask import Flask, render_template
from flask_cors import CORS

from .download import download_video
from .query import query_all_video

DIST_PATH = Path(__file__).parent.parent / "dist"
app = Flask(__name__, template_folder=DIST_PATH, static_folder=DIST_PATH / "assets")

CORS(
    app,
    origins=r"http://localhost:(\d+)?$",
)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/up/<uid>")
def get_up(uid: str):
    videos = query_all_video(uid)
    return orjson.dumps([next(videos) for _ in range(10)])


@app.get("/api/video/<bvid>")
def get_video(bvid: str):
    try:
        download_video(bvid)
        return "success"
    except Exception as e:
        return str(e)
