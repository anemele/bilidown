import axios from "axios";

const request = axios.create({
    baseURL: "http://127.0.0.1:5000/api"
})

export function queryUp(uid: string) {
    return request.get("/up/" + uid)
}

export function downloadVideo(bvid: string) {
    return request.get("/video/" + bvid)
}