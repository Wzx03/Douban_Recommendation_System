<template>
  <div class="insight-container">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card header="🔥 评论关键词云 (NLP 文本挖掘)" shadow="hover">
          <div ref="wordcloudRef" style="height: 350px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card header="📈 情感波动趋势 (LSTM 深度学习识别)" shadow="hover">
          <div ref="trendRef" style="height: 350px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="8">
        <el-card header="🏆 热门评论关键词排行榜" shadow="hover">
          <el-table :data="insightData.top_keywords" style="width: 100%" height="300">
            <el-table-column type="index" label="排名" width="60" />
            <el-table-column prop="word" label="关键词">
              <template #default="scope">
                <el-tag :type="scope.row.type">{{ scope.row.word }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="count" label="频次" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card header="📊 全站评论情感分布" shadow="hover">
          <div ref="pieRef" style="height: 300px;"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card header="🤖 算法底层原理" shadow="hover">
          <div class="algorithm-tip">
            <p><strong>核心算法：</strong> LSTM (长短期记忆网络)</p>
            <p><strong>处理流程：</strong> 评论分词 → 去停用词 → 向量化 → LSTM 特征提取 → Softmax 分类</p>
            <el-divider />
            <p style="color: #666; font-size: 13px;">
              相比于传统朴素贝叶斯，本项目利用 LSTM 强大的序列建模能力，能够有效识别影评中复杂的转折语义和反讽情绪。
            </p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <h3 style="margin-top: 30px; margin-bottom: 20px; color: #333;">💬 真实评论情感判别示例</h3>
    <el-row :gutter="20">
      <el-col :span="6" v-for="(item, index) in insightData.comment_cards" :key="index">
        <el-card class="comment-card" shadow="hover">
          <div class="card-header">
            <span class="movie-name">《{{ item.movie }}》</span>
            <el-tag size="small" :type="item.tag === '正面' ? 'success' : (item.tag === '负面' ? 'danger' : 'warning')">
              {{ item.tag }} {{ item.icon }}
            </el-tag>
          </div>
          <p class="content">"{{ item.content }}"</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref, nextTick } from 'vue';
import * as echarts from 'echarts';
import 'echarts-wordcloud';
import { reqInsight } from '@/api/index.js';

// 使用 ref 机制绑定图表 DOM
const wordcloudRef = ref(null);
const trendRef = ref(null);
const pieRef = ref(null);

const insightData = ref({ top_keywords: [], comment_cards: [] });

let wcChart = null;
let trendChart = null;
let pieChart = null;

const fetchData = async () => {
  try {
    const res = await reqInsight();
    insightData.value = res;

    await nextTick();
    renderCharts(res);
  } catch (error) {
    console.error("洞察数据加载失败", error);
  }
};

const renderCharts = (data) => {
  const wcDom = wordcloudRef.value;
  const trendDom = trendRef.value;
  const pieDom = pieRef.value;

  if (wcDom) {
    if (wcChart) wcChart.dispose();
    wcChart = echarts.init(wcDom);
    wcChart.setOption({
      series: [{
        type: 'wordCloud', shape: 'circle', gridSize: 10, sizeRange: [14, 50],
        rotationRange: [-45, 45],
        textStyle: { color: () => `rgb(${Math.round(Math.random()*160)}, ${Math.round(Math.random()*160)}, ${Math.round(Math.random()*160)})` },
        data: data.wordcloud
      }]
    });
  }

  if (trendDom) {
    if (trendChart) trendChart.dispose();
    trendChart = echarts.init(trendDom);
    trendChart.setOption({
      xAxis: { type: 'category', data: data.trend_chart.months },
      yAxis: { type: 'value', name: '正面情感占比' },
      tooltip: { trigger: 'axis' },
      series: [{ data: data.trend_chart.values, type: 'line', smooth: true, color: '#00B51D', areaStyle: { opacity: 0.1 } }]
    });
  }

  if (pieDom) {
    if (pieChart) pieChart.dispose();
    pieChart = echarts.init(pieDom);
    pieChart.setOption({
      tooltip: { trigger: 'item' },
      legend: { bottom: '5%' },
      series: [{
        type: 'pie', radius: ['40%', '70%'], avoidLabelOverlap: false,
        itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
        label: { show: false }, data: data.sentiment_pie
      }]
    });
  }
};

const handleResize = () => {
  wcChart && wcChart.resize();
  trendChart && trendChart.resize();
  pieChart && pieChart.resize();
};

onMounted(() => {
  fetchData();
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  wcChart && wcChart.dispose();
  trendChart && trendChart.dispose();
  pieChart && pieChart.dispose();
});
</script>

<style scoped>
.insight-container { padding: 10px; }
.algorithm-tip { font-size: 14px; line-height: 1.8; color: #444; }
.comment-card { height: 150px; border-left: 5px solid #00B51D; margin-bottom: 20px; border-radius: 8px;}
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.movie-name { font-weight: bold; font-size: 14px; color: #00B51D; }
.content { font-size: 13px; color: #666; font-style: italic; line-height: 1.5; }
</style>