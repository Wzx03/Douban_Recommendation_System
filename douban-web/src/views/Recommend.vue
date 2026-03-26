<script setup>
import { ref, onMounted } from 'vue';
import { reqRecommend } from '@/api/index.js'; // 🌟 引入统一接口

const list = ref([]);
const isColdStart = ref(false);

const fetchData = async () => {
  const userId = localStorage.getItem('currentUserId') || 1;
  try {
    // 🌟 直接调用接口，不需要再写 url
    const res = await reqRecommend(userId);
    // 因为拦截器已经 return response.data，所以这里直接用 res
    list.value = res.recommendations;
    isColdStart.value = res.recommendations[0]?.is_cold_start || false;
  } catch (error) {
    console.error("推荐列表获取失败", error);
  }
};

onMounted(fetchData);
</script>