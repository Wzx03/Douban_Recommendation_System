<template>
  <div v-if="route.path === '/login'">
    <router-view />
  </div>

  <el-container class="layout-container" v-else>
    <el-header class="top-header">
      <div class="logo-title">
        <el-icon :size="24" style="margin-right: 10px;"><Film /></el-icon>
        基于协同过滤的电影推荐系统
      </div>
      <div class="user-info">
        <el-icon style="margin-right: 5px;"><User /></el-icon>
        <span>当前用户: {{ userName }} (ID: {{ userId }})</span>
      </div>
    </el-header>

    <el-container class="bottom-container">
      <el-aside width="200px" class="aside-menu">
        <el-menu
          :default-active="activeMenu"
          class="el-menu-vertical"
          background-color="#ffffff"
          text-color="#333333"
          active-text-color="#ffffff"
          router
        >
          <el-menu-item index="/home">
            <el-icon><HomeFilled /></el-icon>
            <span>系统首页</span>
          </el-menu-item>

          <el-menu-item index="/recommend">
            <el-icon><Menu /></el-icon>
            <span>个性化推荐</span>
          </el-menu-item>
          <el-menu-item index="/analysis">
            <el-icon><DataAnalysis /></el-icon>
            <span>数据统计大屏</span>
          </el-menu-item>
          <el-menu-item index="/insight">
            <el-icon><ChatLineRound /></el-icon>
            <span>评论情感洞察</span>
          </el-menu-item>

          <el-divider class="menu-divider" />

          <el-menu-item index="/login" @click="handleLogout">
            <el-icon><SwitchButton /></el-icon>
            <span>退出系统</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <el-main class="main-content">
        <div class="breadcrumb-container">
          <el-breadcrumb separator="//">
            <el-breadcrumb-item>豆瓣推荐系统</el-breadcrumb-item>
            <el-breadcrumb-item>{{ pageTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>

        <div class="page-wrapper">
          <router-view />
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
// 🌟 新增引入 HomeFilled 图标
import {
  Film, Menu, DataAnalysis, ChatLineRound,
  SwitchButton, User, HomeFilled, MagicStick
} from '@element-plus/icons-vue';
const route = useRoute();
const router = useRouter();

const userId = computed(() => localStorage.getItem('currentUserId') || '未登录');
const userName = computed(() => localStorage.getItem('currentUserName') || '游客');

const activeMenu = computed(() => route.path);
const pageTitle = computed(() => {
  // 🌟 增加 /home 的中文映射
  const maps = {
  '/home': '系统首页',
  '/recommend': '个性化推荐',
  '/prediction': '评分预测实验室',
  '/analysis': '数据统计大屏',
  '/insight': '评论情感洞察'
  };
  return maps[route.path] || '欢迎使用';
});

const handleLogout = () => {
  localStorage.clear();
  router.push('/login');
};
</script>

<style scoped>
.layout-container { height: 100vh; display: flex; flex-direction: column; }
.top-header { height: 60px; background: linear-gradient(90deg, #56ccf2 0%, #2f80ed 100%); color: white; display: flex; justify-content: space-between; align-items: center; padding: 0 25px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); z-index: 10; }
.logo-title { font-size: 20px; font-weight: bold; letter-spacing: 1px; display: flex; align-items: center; }
.user-info { font-size: 14px; display: flex; align-items: center; }
.bottom-container { flex: 1; overflow: hidden; background-color: #f4f6f9; }
.aside-menu { background-color: #ffffff; border-right: 1px solid #eef0f4; box-shadow: 2px 0 8px rgba(0,0,0,0.02); }
.el-menu-vertical { border-right: none; padding-top: 15px; }
.menu-divider { margin: 15px 0; opacity: 0.5; }
:deep(.el-menu-item) { margin: 5px 10px; border-radius: 6px; transition: all 0.3s ease; }
:deep(.el-menu-item:hover) { background-color: #f0f7ff !important; color: #2f80ed !important; }
:deep(.el-menu-item.is-active) { background-color: #72bbfb !important; color: #ffffff !important; box-shadow: 0 4px 10px rgba(114, 187, 251, 0.4); font-weight: bold; }
.main-content { padding: 20px 25px; display: flex; flex-direction: column; position: relative; }
.main-content::after { content: ''; position: absolute; bottom: 0; right: 0; width: 50vw; height: 50vh; background: radial-gradient(circle at bottom right, rgba(86, 204, 242, 0.15) 0%, transparent 70%); pointer-events: none; z-index: 0; }
.breadcrumb-container { margin-bottom: 20px; font-size: 14px; font-weight: bold; color: #555; position: relative; z-index: 1; }
.page-wrapper { flex: 1; background: #ffffff; border-radius: 10px; padding: 25px; box-shadow: 0 4px 16px rgba(0,0,0,0.04); overflow-y: auto; position: relative; z-index: 1; }
</style>