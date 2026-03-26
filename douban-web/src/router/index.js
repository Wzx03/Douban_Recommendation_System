import { createRouter, createWebHistory } from 'vue-router'
import Recommend from '../views/Recommend.vue'
import Analysis from '../views/Analysis.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/recommend' },
    { path: '/recommend', component: Recommend },
    { path: '/analysis', component: Analysis }
  ]
})

export default router