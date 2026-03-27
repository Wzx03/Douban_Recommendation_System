import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Recommend from '../views/Recommend.vue'
import Analysis from '../views/Analysis.vue'
import Insight from '../views/Insight.vue'
import Home from '../views/Home.vue' // 🌟 新增：引入首页组件
import Prediction from '../views/Prediction.vue'

const routes = [
  {
    path: '/',
    redirect: '/home' // 🌟 修改：默认进入系统首页
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/home', // 🌟 新增：注册首页路由
    name: 'Home',
    component: Home
  },
  {
    path: '/recommend',
    name: 'Recommend',
    component: Recommend
  },
  { path: '/prediction',
    name: 'Prediction',
    component: Prediction
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: Analysis
  },
  {
    path: '/insight',
    name: 'Insight',
    component: Insight
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from) => {
  const isAuthenticated = localStorage.getItem('currentUserId');
  if (to.name !== 'Login' && !isAuthenticated) {
    return { name: 'Login' };
  }
  return true;
})

export default router