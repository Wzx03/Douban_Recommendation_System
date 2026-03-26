<template>
  <div class="recommend-container">
    <el-card class="status-card" shadow="never">
      <div class="status-box">
        <el-tag :type="isColdStart ? 'warning' : 'success'" size="large" effect="dark">
          {{ isColdStart ? '冷启动模式' : '个性化模式' }}
        </el-tag>
        <span class="status-text">
          {{ isColdStart ? '由于您是新用户，系统已为您挑选全站最火的电影' : '算法已根据您的观影历史为您精准锁定以下内容' }}
        </span>
        <el-button type="primary" icon="Refresh" @click="fetchData">刷新换一批</el-button>
      </div>
    </el-card>

    <el-row :gutter="20" class="movie-grid">
      <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="movie in list" :key="movie.movie_id">
        <el-card class="movie-card" :body-style="{ padding: '0px' }" shadow="hover">
          <div class="movie-poster">
            <el-image
              :src="`https://picsum.photos/seed/${movie.movie_id}/300/420`"
              fit="cover"
              class="poster-img"
            />
            <div class="rating-badge">{{ movie.predict_score }}</div>
          </div>
          <div class="movie-detail">
            <div class="movie-title">{{ movie.title }}</div>
            <div class="movie-meta">
              <span>{{ movie.genres }}</span>
              <span class="db-score">豆瓣 {{ movie.actual_douban_score }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
// 这里保持你之前的脚本逻辑，只需确保 list 数据是从 API 获取的即可
import { ref, onMounted } from 'vue';
import axios from 'axios';

const list = ref([]);
const isColdStart = ref(false);

const fetchData = async () => {
  const userId = localStorage.getItem('currentUserId') || 1;
  const res = await axios.get(`http://127.0.0.1:5000/api/recommend/${userId}`);
  list.value = res.data.recommendations;
  // 后端返回的数据中如果有 is_cold_start 字段
  isColdStart.value = res.data.recommendations[0]?.is_cold_start || false;
};

onMounted(fetchData);
</script>

<style scoped>
.status-card { margin-bottom: 20px; border-radius: 8px; }
.status-box { display: flex; align-items: center; gap: 20px; }
.status-text { flex: 1; color: #606266; font-size: 14px; }

.movie-card { margin-bottom: 20px; border-radius: 12px; overflow: hidden; border: none; }
.movie-poster { position: relative; height: 300px; background: #eef1f6; }
.poster-img { width: 100%; height: 100%; }
.rating-badge { position: absolute; top: 10px; right: 10px; background: #ff9900; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; }

.movie-detail { padding: 15px; }
.movie-title { font-weight: bold; font-size: 16px; margin-bottom: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.movie-meta { display: flex; justify-content: space-between; font-size: 12px; color: #999; }
.db-score { color: #f56c6c; font-weight: bold; }
</style>