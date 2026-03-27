<template>
  <div class="analysis-container">
    <el-row :gutter="20" class="top-cards">
      <el-col :span="8">
        <el-card shadow="hover" class="data-card">
          <div class="card-title">均方根误差 (RMSE)</div>
          <div class="card-value">{{ stats.rmse }}</div>
          <div class="card-desc">越接近 0，评分预测越精准</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="data-card">
          <div class="card-title">平均绝对误差 (MAE)</div>
          <div class="card-value">{{ stats.mae }}</div>
          <div class="card-desc">预测分与真实分的平均差距</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="data-card">
          <div class="card-title">用户覆盖率</div>
          <div class="card-value">{{ (stats.coverage * 100).toFixed(1) }}%</div>
          <div class="card-desc">模型能够提供推荐的用户比例</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card shadow="hover">
          <div id="bar-chart" style="height: 400px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <div id="pie-chart" style="height: 400px;"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import * as echarts from 'echarts';
import { reqStatistics } from '@/api/index.js';

const stats = ref({ rmse: 0, mae: 0, coverage: 0 });
let barChart = null;
let pieChart = null;

const fetchData = async () => {
  try {
    const res = await reqStatistics();
    stats.value = res;

    await nextTick();
    renderCharts(res);
  } catch (error) {
    console.error("统计数据获取失败", error);
  }
};

const renderCharts = (data) => {
  const barDom = document.getElementById('bar-chart');
  const pieDom = document.getElementById('pie-chart');

  if (barDom) {
    if (barChart) barChart.dispose();
    barChart = echarts.init(barDom);
    barChart.setOption({
      title: { text: '系统原始评分分布', left: 'center' },
      xAxis: { type: 'category', data: ['2分', '4分', '6分', '8分', '10分'] },
      yAxis: { type: 'value' },
      series: [{ data: data.rating_distribution, type: 'bar', itemStyle: { color: '#00B51D' } }]
    });
  }

  if (pieDom) {
    if (pieChart) pieChart.dispose();
    pieChart = echarts.init(pieDom);
    const pieData = Object.keys(data.genre_distribution).map(key => ({
      name: key, value: data.genre_distribution[key]
    }));
    pieChart.setOption({
      title: { text: '豆瓣电影类型占比', left: 'center' },
      tooltip: { trigger: 'item' },
      series: [{ type: 'pie', radius: '50%', data: pieData }]
    });
  }
};

const handleResize = () => {
  barChart && barChart.resize();
  pieChart && pieChart.resize();
};

onMounted(() => {
  fetchData();
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  barChart && barChart.dispose();
  pieChart && pieChart.dispose();
});
</script>

<style scoped>
.analysis-container { padding: 10px; }
.top-cards { margin-bottom: 20px; }
.data-card { text-align: center; padding: 20px 0; border-radius: 8px; }
.card-title { font-size: 15px; color: #666; margin-bottom: 12px; }
.card-value { font-size: 38px; font-weight: bold; color: #00B51D; margin-bottom: 12px; }
.card-desc { font-size: 13px; color: #999; }
.chart-row { margin-top: 20px; }
</style>