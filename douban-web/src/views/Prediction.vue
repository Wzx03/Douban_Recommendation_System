<template>
  <div class="prediction-container">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card shadow="never" class="search-card">
          <template #header>
            <div class="card-header">
              <span>🔍 查找目标电影</span>
            </div>
          </template>
          <el-input
            v-model="searchKey"
            placeholder="输入电影名称关键字..."
            clearable
            @input="handleSearch"
          >
            <template #append><el-icon><Search /></el-icon></template>
          </el-input>

          <div class="search-results" v-loading="searching">
            <div
              v-for="m in searchList"
              :key="m.movie_id"
              class="search-item"
              :class="{active: selectedMovie?.movie_id === m.movie_id}"
              @click="selectMovie(m)"
            >
              <div class="m-info">
                <p class="m-name">{{ m.title }}</p>
                <p class="m-genre">{{ m.genres }}</p>
              </div>
              <el-tag size="small">{{ m.douban_score }}分</el-tag>
            </div>
            <el-empty v-if="!searchList.length" description="暂无搜索结果" :image-size="60" />
          </div>
        </el-card>
      </el-col>

      <el-col :span="16">
        <el-card shadow="never" class="lab-card">
          <div v-if="selectedMovie" class="lab-content">
            <div class="movie-intro">
              <el-image
                :src="`https://picsum.photos/seed/${selectedMovie.movie_id}/200/280`"
                class="lab-poster"
              />
              <div class="lab-text">
                <h2>{{ selectedMovie.title }}</h2>
                <el-descriptions :column="1" border>
                  <el-descriptions-item label="电影类型">{{ selectedMovie.genres }}</el-descriptions-item>
                  <el-descriptions-item label="豆瓣真实评分">
                    <el-rate v-model="selectedMovie.douban_score" disabled show-score :max="10" />
                  </el-descriptions-item>
                </el-descriptions>
                <el-button
                  type="primary"
                  size="large"
                  icon="Cpu"
                  class="predict-btn"
                  @click="startPredict"
                  :loading="predicting"
                >
                  启动 SVD 算法进行预测
                </el-button>
              </div>
            </div>

            <el-divider>算法推理结果</el-divider>

            <div class="result-display" v-if="predictionResult">
              <div class="score-circle">
                <el-progress
                  type="dashboard"
                  :percentage="predictionResult.predicted_rating * 10"
                  :color="colors"
                  :width="180"
                >
                  <template #default="{ percentage }">
                    <span class="percentage-value">{{ (percentage / 10).toFixed(1) }}</span>
                    <span class="percentage-label">系统预测分</span>
                  </template>
                </el-progress>
              </div>
              <div class="analysis-box">
                <p class="analysis-title">✨ 算法分析结论</p>
                <p class="analysis-text">
                  基于 SVD 矩阵分解模型，结合您的历史偏好向量 $p_u$ 与该电影的特征向量 $q_i$，
                  我们预测您对这部电影的喜爱程度为 <strong>{{ predictionResult.predicted_rating }}</strong> 分。
                  该结果与豆瓣真实分数相差仅 <strong>{{ Math.abs(predictionResult.predicted_rating - selectedMovie.douban_score).toFixed(2) }}</strong> 分。
                </p>
              </div>
            </div>
          </div>
          <el-empty v-else description="请从左侧搜索并选择一部电影开始实验" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { Search, Cpu } from '@element-plus/icons-vue';
import { reqSearchMovies, reqMovieDetail } from '@/api/index.js';

const searchKey = ref('');
const searching = ref(false);
const searchList = ref([]);
const selectedMovie = ref(null);
const predicting = ref(false);
const predictionResult = ref(null);

const colors = [
  { color: '#f56c6c', percentage: 40 },
  { color: '#e6a23c', percentage: 70 },
  { color: '#67c23a', percentage: 100 },
];

const handleSearch = async () => {
  if (!searchKey.value) return;
  searching.value = true;
  const res = await reqSearchMovies(searchKey.value);
  searchList.value = res.movies;
  searching.value = false;
};

const selectMovie = (m) => {
  selectedMovie.value = m;
  predictionResult.value = null;
};

const startPredict = async () => {
  predicting.value = true;
  const userId = localStorage.getItem('currentUserId');
  // 模拟算法计算延迟，增加“仪式感”
  setTimeout(async () => {
    const res = await reqMovieDetail(selectedMovie.value.movie_id, userId);
    predictionResult.value = res;
    predicting.value = false;
  }, 800);
};
</script>

<style scoped>
.search-card { height: 75vh; }
.search-results { margin-top: 15px; height: calc(100% - 60px); overflow-y: auto; }
.search-item {
  display: flex; justify-content: space-between; align-items: center;
  padding: 12px; border-bottom: 1px solid #f0f0f0; cursor: pointer; border-radius: 8px;
}
.search-item:hover { background-color: #f5f7fa; }
.search-item.active { background-color: #ecf5ff; border: 1px solid #409eff; }
.m-name { font-weight: bold; margin: 0 0 5px 0; font-size: 14px; }
.m-genre { font-size: 12px; color: #999; margin: 0; }

.lab-card { height: 75vh; display: flex; align-items: center; justify-content: center; }
.lab-content { width: 100%; }
.movie-intro { display: flex; gap: 30px; margin-bottom: 30px; }
.lab-poster { width: 180px; height: 250px; border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.15); }
.lab-text { flex: 1; }
.predict-btn { margin-top: 25px; width: 100%; font-weight: bold; }

.result-display { display: flex; align-items: center; gap: 50px; padding: 20px; background: #fdfdfd; border-radius: 15px; }
.percentage-value { display: block; font-size: 38px; font-weight: bold; color: #2f80ed; }
.percentage-label { font-size: 14px; color: #999; }
.analysis-box { flex: 1; background: #fff; padding: 20px; border-left: 4px solid #2f80ed; border-radius: 4px; box-shadow: 0 2px 12px rgba(0,0,0,0.03); }
.analysis-title { font-weight: bold; color: #333; margin-top: 0; }
.analysis-text { font-size: 14px; color: #666; line-height: 1.8; }
</style>