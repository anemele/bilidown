<template>
  <div class="about">
    <p>输入视频的的av号或BV号，下载该视频</p>

    <div class="input-box">
      <el-input type="text" v-model="bvid" placeholder="请输入bvid" style="margin-right: 10px;">
      </el-input>
      <el-button @click="download">下载</el-button>
    </div>


  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { downloadVideo } from '@/api'

const bvid = ref('')

async function download() {
  let msg = (await downloadVideo(bvid.value)).data;
  alert(msg);
}

</script>

<style scoped>
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
}
</style>
