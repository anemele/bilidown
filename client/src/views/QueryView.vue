<template>
  <div class="about">
    <p>输入UP的uid，查询所有投稿视频信息</p>

    <div class="input-box">
      <el-input v-model="uid" placeholder="请输入UP的uid" style="margin-right: 10px;"></el-input>
      <el-button type="primary" @click="query">查询</el-button>
    </div>

    <div>
      <li v-for="(item, index) in data" :key="index">
        <VideoItem :video="item"></VideoItem>
      </li>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { queryUp } from '@/api';
import { type Video, type QueryResult } from "@/types";
import VideoItem from '@/components/VideoItem.vue';

let uid = ref('');
let data = reactive<Video[]>([]);

function formatDate(date: number): string {
  const d = new Date(date * 1000);
  const year = d.getFullYear();
  const month = d.getMonth() + 1;
  const day = d.getDate();
  const hour = d.getHours();
  const minute = d.getMinutes();
  const second = d.getSeconds();
  return `${year}-${month < 10 ? '0' + month : month}-${day < 10 ? '0' + day : day} ${hour < 10 ? '0' + hour : hour}:${minute < 10 ? '0' + minute : minute}:${second < 10 ? '0' + second : second}`;
}

const query = () => {
  if (uid.value === '') { alert('请输入UP的uid'); return; }
  data.length = 0;

  queryUp(uid.value).then(res => {
    if (res.data.length === 0) { alert(`没有查询到 ${uid.value} 相关视频`); return; }

    res.data.forEach((video: QueryResult) => {
      data.push({
        title: video.title,
        pubdate: formatDate(video.created),
        view: video.play,
        reply: video.comment,
        bvid: video.bvid,
      });
    });
  });
};
</script>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
}

.input-box {
  display: flex;
  justify-content: space-between;
}</style>
