<template>
  <div class="home-container">
    <div class="welcome-banner">
      <div class="banner-content">
        <h2>🎬 欢迎探索豆瓣电影大世界</h2>
        <p>基于海量真实用户评分数据，挖掘全站最高分神作，发现你的下一部挚爱。</p>
      </div>
      <div class="banner-stats">
        <div class="stat-item">
          <span class="stat-value">100+</span>
          <span class="stat-label">入库类型</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">TOP 100</span>
          <span class="stat-label">高分金榜</span>
        </div>
      </div>
    </div>

    <el-card class="list-card" shadow="never">
      <el-tabs v-model="activeGenre" @tab-change="handleTabChange" class="genre-tabs">
        <el-tab-pane v-for="g in genres" :key="g" :label="g" :name="g"></el-tab-pane>
      </el-tabs>

      <div v-loading="loading" class="movie-grid">
        <el-row :gutter="20">
          <el-col :xs="12" :sm="8" :md="6" :lg="4" :xl="3" v-for="(movie, index) in movies" :key="movie.movie_id">
            <el-card class="movie-card" :body-style="{ padding: '0px' }" shadow="hover">
              <div class="movie-poster">
                <div class="rank-badge" :class="'rank-' + (index + 1)">TOP {{ index + 1 }}</div>
                <el-image
                  :src="`https://picsum.photos/seed/${movie.movie_id}/300/420`"
                  fit="cover"
                  class="poster-img"
                  loading="lazy"
                />
                <div class="rating-badge">{{ movie.douban_score.toFixed(1) }}</div>
              </div>
              <div class="movie-detail">
                <div class="movie-title" :title="movie.title">{{ movie.title }}</div>
                <div class="movie-meta">{{ movie.genres }}</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { reqTopMovies } from '@/api/index.js';

const activeGenre = ref('全部');
// 换成你真实数据集中排名前 10 的核心类型
const genres = ['全部', '剧情', '爱情', '喜剧', '动作', '犯罪', '悬疑', '惊悚', '科幻', '冒险', '奇幻'];
const movies = ref([]);
const loading = ref(false);

const fetchMovies = async (genre) => {
  loading.value = true;
  try {
    const res = await reqTopMovies(genre, 100);
    movies.value = res.movies;
  } catch (error) {
    console.error('获取高分榜单失败', error);
  } finally {
    loading.value = false;
  }
};

const handleTabChange = (name) => {
  fetchMovies(name);
};

onMounted(() => {
  fetchMovies('全部');
});
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

/* 横幅样式 */
.welcome-banner {
  background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);
  border-radius: 12px;
  padding: 30px 40px;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 8px 20px rgba(43, 88, 118, 0.2);
}

.banner-content h2 { margin: 0 0 10px 0; font-size: 26px; }
.banner-content p { margin: 0; font-size: 15px; opacity: 0.85; }

.banner-stats { display: flex; gap: 30px; }
.stat-item { text-align: center; }
.stat-value { display: block; font-size: 28px; font-weight: bold; color: #ffd700; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }
.stat-label { font-size: 12px; opacity: 0.8; margin-top: 5px; display: block; }

/* 榜单卡片 */
.list-card { border: none; border-radius: 12px; }
.genre-tabs { margin-bottom: 20px; }

/* 电影卡片 */
.movie-card { margin-bottom: 20px; border-radius: 10px; overflow: hidden; border: none; transition: transform 0.3s; }
.movie-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important; }

.movie-poster { position: relative; height: 320px; background: #eef1f6; overflow: hidden; }
.poster-img { width: 100%; height: 100%; transition: transform 0.5s; }
.movie-card:hover .poster-img { transform: scale(1.05); }

/* 右下角豆瓣评分角标 */
.rating-badge { position: absolute; bottom: 10px; right: 10px; background: rgba(0, 0, 0, 0.7); color: #ffd700; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 14px; backdrop-filter: blur(4px); }

/* 左上角排名角标 */
.rank-badge { position: absolute; top: 0; left: 0; background: #909399; color: white; padding: 6px 12px; font-weight: bold; font-size: 13px; border-bottom-right-radius: 10px; z-index: 2; box-shadow: 2px 2px 8px rgba(0,0,0,0.2); }
/* 前三名专属尊贵颜色 */
.rank-1 { background: linear-gradient(45deg, #ff416c, #ff4b2b); }
.rank-2 { background: linear-gradient(45deg, #f7971e, #ffd200); }
.rank-3 { background: linear-gradient(45deg, #00b09b, #96c93d); }

.movie-detail { padding: 15px; background: #fff; }
.movie-title { font-weight: bold; font-size: 16px; margin-bottom: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: #333; }
.movie-meta { font-size: 12px; color: #888; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
</style>