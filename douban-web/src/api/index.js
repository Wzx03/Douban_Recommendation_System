import axios from 'axios';

const request = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  timeout: 10000
});

request.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('API 请求出错:', error);
    return Promise.reject(error);
  }
);

export const reqLogin = (data) => request.post('/login', data);
export const reqRegister = (data) => request.post('/register', data);

// 🌟 新增：请求首页 Top100 与分类电影榜单
export const reqTopMovies = (genre = '全部', limit = 100) =>
  request.get(`/home/top_movies`, { params: { genre, limit } });

export const reqRecommend = (userId, topN = 10) => request.get(`/recommend/${userId}?top_n=${topN}`);
export const reqStatistics = () => request.get('/statistics');
export const reqInsight = () => request.get('/insight');
export const reqMovieDetail = (movieId, userId) => request.get(`/movie/${movieId}`, { params: { user_id: userId } });
//export const reqMovieDetail = (movieId, userId) => request.get(`/movie/${movieId}`, { params: { user_id: userId } });
export const reqSearchMovies = (keyword) => request.get('/movies/search', { params: { keyword } });
export const reqWordcloud = (userId) => request.get(`/user/${userId}/wordcloud`);

export default request;