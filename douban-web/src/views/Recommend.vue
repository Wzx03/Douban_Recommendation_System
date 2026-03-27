<template>
  <div class="recommend-container">
    <el-card class="status-card" shadow="never">
      <div class="status-box">
        <div class="status-info">
          <el-tag :type="algoType.includes('内容') ? 'warning' : 'success'" effect="dark" round size="large">
            <el-icon style="margin-right: 5px;"><component :is="algoType.includes('内容') ? 'Cpu' : 'Share'" /></el-icon>
            {{ algoType }}
          </el-tag>
          <span class="status-text">{{ recReason }}</span>
        </div>
        <el-button type="primary" color="#2f80ed" round icon="Refresh" @click="fetchData" :loading="loading">
          刷新换一批
        </el-button>
      </div>
    </el-card>

    <div v-if="loading" class="movie-grid">
      <el-row :gutter="20">
        <el-col :xs="12" :sm="8" :md="6" :lg="4" :xl="3" v-for="i in 12" :key="i">
          <el-skeleton style="width: 100%; margin-bottom: 20px;" animated>
            <template #template>
              <el-skeleton-item variant="image" style="width: 100%; height: 260px; border-radius: 10px;" />
              <div style="padding: 10px 0;">
                <el-skeleton-item variant="h3" style="width: 70%;" />
                <el-skeleton-item variant="text" style="width: 40%;" />
              </div>
            </template>
          </el-skeleton>
        </el-col>
      </el-row>
    </div>

    <div v-else class="movie-grid">
      <el-row :gutter="20">
        <el-col :xs="12" :sm="8" :md="6" :lg="4" :xl="3" v-for="movie in list" :key="movie.movie_id">
          <el-card class="movie-card" :body-style="{ padding: '0px' }" shadow="hover">
            <div class="movie-poster">
              <div class="match-badge" :class="getMatchClass(movie.predict_score)">
                {{ (movie.predict_score * 10).toFixed(0) }}% 匹配
              </div>

              <el-image
                :src="movie.cover_url || `https://picsum.photos/seed/${movie.movie_id}/300/400`"
                fit="cover"
                class="poster-img"
                loading="lazy"
              />

              <div class="rating-badge">豆瓣 {{ movie.actual_douban_score.toFixed(1) }}</div>
            </div>

            <div class="movie-detail">
              <div class="movie-title" :title="movie.title">{{ movie.title }}</div>
              <div class="movie-meta">{{ movie.genres }}</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { reqRecommend } from '@/api/index.js';
import { Warning, MagicStick, Refresh, Cpu, Share } from '@element-plus/icons-vue';

const list = ref([]);
const loading = ref(true);
const algoType = ref('算法加载中...');
const recReason = ref('...');

const fetchData = async () => {
  loading.value = true;
  const userId = localStorage.getItem('currentUserId') || 1;
  try {
    // 请求 12 条数据填满两行
    const res = await reqRecommend(userId, 12);
    list.value = res.recommendations;

    // 动态提取系统当前使用的算法和解释文案
    if(res.recommendations.length > 0) {
      algoType.value = res.recommendations[0].algo_type;
      recReason.value = res.recommendations[0].reason;
    }
  } catch (error) {
    console.error("推荐列表获取失败", error);
  } finally {
    // 稍微延迟关闭以展示骨架屏的高级感
    setTimeout(() => {
      loading.value = false;
    }, 500);
  }
};

// 根据预测分动态返回匹配度颜色
const getMatchClass = (score) => {
  if (score >= 8.5) return 'match-high';
  if (score >= 7.0) return 'match-mid';
  return 'match-low';
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.recommend-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 顶部状态卡片 */
.status-card {
  border: none;
  border-radius: 12px;
  background: linear-gradient(to right, #ffffff, #f0f7ff);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
}

.status-box {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 10px;
}

.status-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.status-text {
  color: #555;
  font-size: 14px;
  font-weight: 500;
}

/* 电影卡片 */
.movie-card {
  margin-bottom: 20px;
  border-radius: 10px;
  overflow: hidden;
  border: none;
  transition: transform 0.3s;
}

.movie-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(47, 128, 237, 0.15) !important;
}

.movie-poster {
  position: relative;
  height: 260px;
  background: #eef1f6;
  overflow: hidden;
}

.poster-img {
  width: 100%;
  height: 100%;
  transition: transform 0.5s;
}

.movie-card:hover .poster-img {
  transform: scale(1.05);
}

/* 匹配度角标 (Netflix 风格) */
.match-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: bold;
  font-size: 12px;
  z-index: 2;
  color: white;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}
.match-high { background-color: #67C23A; } /* 绿色 */
.match-mid { background-color: #E6A23C; } /* 橙色 */
.match-low { background-color: #909399; } /* 灰色 */

/* 右下角真实豆瓣评分 */
.rating-badge {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.7);
  color: #ffd700;
  padding: 4px 8px;
  border-radius: 6px;
  font-weight: bold;
  font-size: 12px;
  backdrop-filter: blur(4px);
  z-index: 2;
}

.movie-detail {
  padding: 12px;
  background: #fff;
}

.movie-title {
  font-weight: bold;
  font-size: 15px;
  margin-bottom: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #333;
}

.movie-meta {
  font-size: 12px;
  color: #888;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>