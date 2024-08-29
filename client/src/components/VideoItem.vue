<template>
    <a :href="`https://www.bilibili.com/video/${video.bvid}`" target="_blank">{{ video.title }}</a>
    <p>发布于：{{ video.pubdate }}</p>
    <p>播放量：{{ video.view }}</p>
    <p>评论数：{{ video.reply }}</p>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import { type Video } from '@/types';

defineProps<{ video: Video }>();

</script>

<style scoped></style>