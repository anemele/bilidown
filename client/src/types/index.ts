export interface Video {
    title: string;
    pubdate: string;
    view: number;
    // danmaku: number;
    bvid: string;
    reply: number;
}

export interface QueryResult {
    title: string;
    created: number;
    play: number;
    comment: number;
    bvid: string;
}