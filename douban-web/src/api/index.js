import axios from 'axios';

// 1. 创建统一的 Axios 实例
const request = axios.create({
  baseURL: 'http://127.0.0.1:5000/api', // 🌟 这里统一配置，以后换服务器只改这里
  timeout: 10000
});

// 2. 响应拦截器：自动剥离 axios 的包裹层，直接返回真实数据
request.interceptors.response.use(
  (response) => {
    return response.data; // 脱去 data 外壳，后面的 vue 页面不需要再写 res.data
  },
  (error) => {
    console.error('API 请求出错:', error);
    return Promise.reject(error);
  }
);

// 3. 统一导出所有业务接口 (规范命名：req开头代表请求)
export const reqLogin = (data) => request.post('/login', data);
export const reqRegister = (data) => request.post('/register', data);

export const reqRecommend = (userId, topN = 10) => request.get(`/recommend/${userId}?top_n=${topN}`);
export const reqStatistics = () => request.get('/statistics');
export const reqInsight = () => request.get('/insight');
export const reqMovieDetail = (movieId, userId) => request.get(`/movie/${movieId}`, { params: { user_id: userId } });
export const reqWordcloud = (userId) => request.get(`/user/${userId}/wordcloud`);

export default request;