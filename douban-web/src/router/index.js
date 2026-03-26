import { createRouter, createWebHistory } from 'vue-router'
// 1. 导入所有的页面组件
import Login from '../views/Login.vue'
import Recommend from '../views/Recommend.vue'
import Analysis from '../views/Analysis.vue'
import Insight from '../views/Insight.vue' // 🌟 修复：引入刚才写好的评论洞察页面

const routes = [
  {
    path: '/',
    redirect: '/login'
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
  },
  {
    path: '/insight', // 🌟 修复：注册 /insight 路由映射
    name: 'Insight',
    component: Insight
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 🌟 修复：使用 Vue Router 4 官方推荐的 return 写法，消除控制台 next() 黄色警告
router.beforeEach((to, from) => {
  const isAuthenticated = localStorage.getItem('currentUserId');

  // 如果去的不是登录页，且没有登录，强制重定向到登录页
  if (to.name !== 'Login' && !isAuthenticated) {
    return { name: 'Login' };
  }

  // 验证通过，默认放行 (不需要再写 next() 啦)
  return true;
})

export default router