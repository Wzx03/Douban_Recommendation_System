import axios from 'axios';
import { ElMessage } from 'element-plus';

const request = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 5000
});

// 响应拦截器：处理错误
request.interceptors.response.use(
  res => res.data,
  err => {
    ElMessage.error(err.response?.data?.message || '网络连接失败');
    return Promise.reject(err);
  }
);

export const getRecommendations = (userId, topN = 10) => request.get(`/recommend/${userId}?top_n=${topN}`);
export const getMovieDetail = (id) => request.get(`/movie/${id}`);
export const submitRating = (data) => request.post('/rating', data);
export const getStatistics = () => request.get('/statistics');
export const getSentiment = (id) => request.get(`/movie/${id}/sentiment`);