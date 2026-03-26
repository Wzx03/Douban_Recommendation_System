<template>
  <div class="recommend-container">
    <div class="header">
      <el-select v-model="userId" placeholder="请选择/输入用户ID" filterable @change="fetchData">
        <el-option v-for="i in 10" :key="i" :label="'用户 ' + i" :value="i" />
      </el-select>
      <el-button type="primary" @click="fetchData" :loading="loading" style="margin-left: 10px">
        生成个性化推荐
      </el-button>
    </div>

    <el-skeleton :loading="loading" animated :count="3">
      <template #template>
        <el-skeleton-item variant="rect" style="height: 200px; margin-bottom: 20px" />
      </template>
      <template #default>
        <el-row :gutter="20">
          <el-col v-for="movie in movieList" :key="movie.movie_id" :xs="24" :sm="12" :md="6" :lg="4.8">
            <el-card class="movie-card" @click="goToDetail(movie.movie_id)">
              <div class="score-badge">预测 {{ movie.predicted_rating }}</div>
              <img src="https://via.placeholder.com/150x220?text=Movie+Cover" class="cover" />
              <div class="info">
                <h4 class="title">{{ movie.title }}</h4>
                <p class="genres">{{ movie.genres }}</p>
                <div class="scores">
                  <span class="douban">豆瓣 {{ movie.douban_score }}</span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </template>
    </el-skeleton>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getRecommendations } from '@/api';

const userId = ref(1);
const movieList = ref([]);
const loading = ref(false);
const router = useRouter();

const fetchData = async () => {
  loading.value = true;
  try {
    const res = await getRecommendations(userId.value);
    movieList.value = res.recommendations;
  } finally {
    loading.value = false;
  }
};

const goToDetail = (id) => router.push(`/movie/${id}`);

onMounted(fetchData);
</script>

<style scoped>
.movie-card { margin-bottom: 20px; cursor: pointer; position: relative; transition: transform 0.3s; }
.movie-card:hover { transform: translateY(-5px); }
.score-badge { position: absolute; top: 10px; right: 10px; background: #00B51D; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; z-index: 10; }
.cover { width: 100%; border-radius: 4px; }
.title { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin: 10px 0 5px; }
.genres { font-size: 12px; color: #999; }
.douban { color: #ff9900; font-weight: bold; }
</style>