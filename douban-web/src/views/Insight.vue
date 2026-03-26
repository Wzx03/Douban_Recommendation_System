<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import * as echarts from 'echarts';
import 'echarts-wordcloud';
import { reqInsight } from '@/api/index.js'; // 🌟 引入统一接口

const insightData = ref({ top_keywords: [], comment_cards: [] });

let wcChart = null;
let trendChart = null;
let pieChart = null;

const fetchData = async () => {
  try {
    const res = await reqInsight(); // 🌟 直接调用
    insightData.value = res;
    renderCharts(res);
  } catch (error) {
    console.error("洞察数据加载失败", error);
  }
};

const renderCharts = (data) => {
  wcChart = echarts.init(document.getElementById('wordcloud-box'));
  wcChart.setOption({
    series: [{
      type: 'wordCloud', shape: 'circle', gridSize: 10, sizeRange: [14, 50],
      rotationRange: [-45, 45],
      textStyle: { color: () => `rgb(${Math.round(Math.random()*160)}, ${Math.round(Math.random()*160)}, ${Math.round(Math.random()*160)})` },
      data: data.wordcloud
    }]
  });

  trendChart = echarts.init(document.getElementById('trend-box'));
  trendChart.setOption({
    xAxis: { type: 'category', data: data.trend_chart.months },
    yAxis: { type: 'value', name: '正面情感占比' },
    tooltip: { trigger: 'axis' },
    series: [{ data: data.trend_chart.values, type: 'line', smooth: true, color: '#00B51D', areaStyle: { opacity: 0.1 } }]
  });

  pieChart = echarts.init(document.getElementById('pie-box'));
  pieChart.setOption({
    tooltip: { trigger: 'item' },
    legend: { bottom: '5%' },
    series: [{
      type: 'pie', radius: ['40%', '70%'], avoidLabelOverlap: false,
      itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
      label: { show: false }, data: data.sentiment_pie
    }]
  });
};

// 🌟 图表自适应处理
const handleResize = () => {
  if (wcChart) wcChart.resize();
  if (trendChart) trendChart.resize();
  if (pieChart) pieChart.resize();
};

onMounted(() => {
  fetchData();
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
});
</script>