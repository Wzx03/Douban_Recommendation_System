import { createRouter, createWebHistory } from 'vue-router'
// 导入你的页面组件
import Login from '../views/Login.vue'
import Recommend from '../views/Recommend.vue'
import Analysis from '../views/Analysis.vue'

const routes = [
  {
    path: '/',
    redirect: '/login' // 🌟 一进来就重定向到登录页
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/recommend',
    name: 'Recommend',
    component: Recommend
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: Analysis
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 🌟 新增：路由守卫 (未登录不让进推荐页)
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('currentUserId');
  if (to.name !== 'Login' && !isAuthenticated) {
    next({ name: 'Login' });
  } else {
    next();
  }
})

export default router