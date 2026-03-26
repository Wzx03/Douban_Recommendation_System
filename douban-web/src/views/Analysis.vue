<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import { reqStatistics } from '@/api/index.js'; // 🌟 引入统一接口

const stats = ref({ rmse: 0, mae: 0, coverage: 0 });
let barChart = null;
let pieChart = null;

const fetchData = async () => {
  try {
    const res = await reqStatistics(); // 🌟 直接调用
    stats.value = res;
    renderCharts(res);
  } catch (error) {
    console.error("统计数据获取失败", error);
  }
};

const renderCharts = (data) => {
  barChart = echarts.init(document.getElementById('bar-chart'));
  barChart.setOption({
    title: { text: '系统原始评分分布', left: 'center' },
    xAxis: { type: 'category', data: ['2分', '4分', '6分', '8分', '10分'] },
    yAxis: { type: 'value' },
    series: [{ data: data.rating_distribution, type: 'bar', itemStyle: { color: '#00B51D' } }]
  });

  pieChart = echarts.init(document.getElementById('pie-chart'));
  const pieData = Object.keys(data.genre_distribution).map(key => ({
    name: key, value: data.genre_distribution[key]
  }));
  pieChart.setOption({
    title: { text: '豆瓣电影类型占比', left: 'center' },
    tooltip: { trigger: 'item' },
    series: [{ type: 'pie', radius: '50%', data: pieData }]
  });
};

// 🌟 新增：让 ECharts 随窗口动态缩放
const handleResize = () => {
  if (barChart) barChart.resize();
  if (pieChart) pieChart.resize();
};

onMounted(() => {
  fetchData();
  window.addEventListener('resize', handleResize);
});

// 🌟 销毁时移除监听器，防止内存泄漏
onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
});
</script>