<template>
  <div class="analysis-container">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card shadow="hover" class="metric-card">
          <template #header><div class="card-header"><span>均方根误差 (RMSE)</span></div></template>
          <div class="metric-value">{{ metrics.rmse }}</div>
          <div class="metric-desc">越接近 0，评分预测越精准</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="metric-card">
          <template #header><div class="card-header"><span>平均绝对误差 (MAE)</span></div></template>
          <div class="metric-value">{{ metrics.mae }}</div>
          <div class="metric-desc">预测分与真实分的平均差距</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="metric-card">
          <template #header><div class="card-header"><span>用户覆盖率</span></div></template>
          <div class="metric-value">{{ (metrics.coverage * 100).toFixed(1) }}%</div>
          <div class="metric-desc">模型能够提供推荐的用户比例</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 25px;">
      <el-col :span="12">
        <el-card shadow="always">
          <div id="ratingChart" style="height: 400px; width: 100%;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="always">
          <div id="genreChart" style="height: 400px; width: 100%;"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import * as echarts from 'echarts';
import { getStatistics } from '@/api'; // 确保你的 api/index.js 有这个函数

const metrics = ref({ rmse: 0.92, mae: 0.72, coverage: 0.85 });

onMounted(async () => {
  // 模拟从后端获取统计数据，实际可开启下面这行
  // const data = await getStatistics();

  // 初始化评分分布柱状图
  const rChart = echarts.init(document.getElementById('ratingChart'));
  rChart.setOption({
    title: { text: '系统原始评分分布', left: 'center' },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ['2分', '4分', '6分', '8分', '10分'] },
    yAxis: { type: 'value' },
    series: [{
      data: [120, 450, 890, 1200, 600],
      type: 'bar',
      itemStyle: { color: '#00B51D' }
    }]
  });

  // 初始化类型占比饼图
  const gChart = echarts.init(document.getElementById('genreChart'));
  gChart.setOption({
    title: { text: '豆瓣电影类型占比', left: 'center' },
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: '50%',
      data: [
        { value: 1048, name: '剧情' },
        { value: 735, name: '喜剧' },
        { value: 580, name: '动作' },
        { value: 484, name: '科幻' },
        { value: 300, name: '爱情' }
      ]
    }]
  });

  // 响应式窗口缩放
  window.addEventListener('resize', () => {
    rChart.resize();
    gChart.resize();
  });
});
</script>

<style scoped>
.analysis-container { padding: 20px; }
.metric-card { text-align: center; border-top: 4px solid #00B51D; }
.metric-value { font-size: 36px; font-weight: bold; color: #00B51D; margin: 10px 0; }
.metric-desc { font-size: 13px; color: #909399; }
</style>