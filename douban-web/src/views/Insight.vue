<template>
  <div class="insight-container">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card header="🔥 评论热词画像 (NLP 词频统计)" shadow="hover">
          <div id="wordcloud-box" style="height: 350px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card header="📈 情感变动趋势 (LSTM 月度追踪)" shadow="hover">
          <div id="trend-box" style="height: 350px;"></div>
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
        <el-card header="📊 全站评论情感分布 (LSTM 判别结果)" shadow="hover">
          <div id="pie-box" style="height: 300px;"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card header="💡 算法洞察提示" shadow="hover">
          <div class="algorithm-tip">
            <p><strong>底层模型：</strong> 基于 LSTM 的双向循环神经网络</p>
            <p><strong>训练数据：</strong> 豆瓣 10万+ 真实短评</p>
            <p><strong>准确率：</strong> 验证集 89.4%</p>
            <el-divider />
            <p style="color: #666; font-size: 13px;">
              该模块通过对文本进行分词、去停用词，利用 LSTM 提取语义特征，能够精准识别评论背后的情绪波动。
            </p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <h3 style="margin-top: 30px; color: #333;">💬 真实评论情感判别示例</h3>
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
import { onMounted, ref } from 'vue';
import * as echarts from 'echarts';
import 'echarts-wordcloud'; // 🌟 需安装此插件：npm install echarts-wordcloud
import axios from 'axios';

const insightData = ref({ top_keywords: [], comment_cards: [] });

const fetchData = async () => {
  const res = await axios.get('http://127.0.0.1:5000/api/insight');
  insightData.value = res.data;

  // 渲染图表
  renderCharts(res.data);
};

const renderCharts = (data) => {
  // 1. 词云
  const wcChart = echarts.init(document.getElementById('wordcloud-box'));
  wcChart.setOption({
    series: [{
      type: 'wordCloud',
      data: data.wordcloud,
      textStyle: { color: () => `rgb(${Math.round(Math.random() * 160)}, ${Math.round(Math.random() * 160)}, ${Math.round(Math.random() * 160)})` }
    }]
  });

  // 2. 趋势图
  const trendChart = echarts.init(document.getElementById('trend-box'));
  trendChart.setOption({
    xAxis: { type: 'category', data: data.trend_chart.months },
    yAxis: { type: 'value', name: '正面情感占比' },
    series: [{ data: data.trend_chart.values, type: 'line', smooth: true, color: '#00B51D' }]
  });

  // 3. 饼图
  const pieChart = echarts.init(document.getElementById('pie-box'));
  pieChart.setOption({
    tooltip: { trigger: 'item' },
    series: [{ type: 'pie', radius: '70%', data: data.sentiment_pie }]
  });
};

onMounted(fetchData);
</script>

<style scoped>
.insight-container { padding: 5px; }
.algorithm-tip { font-size: 14px; line-height: 1.8; color: #333; }
.comment-card { height: 160px; margin-bottom: 20px; border-left: 5px solid #00B51D; }
.card-header { display: flex; justify-content: space-between; margin-bottom: 10px; }
.movie-name { font-weight: bold; font-size: 14px; color: #00B51D; }
.content { font-size: 13px; color: #666; font-style: italic; }
</style>