<template>
  <el-container class="layout-container">
    <el-aside width="220px" class="aside">
      <div class="logo">
        <el-icon :size="22" color="#fff"><Film /></el-icon>
        <span>豆瓣推荐系统</span>
      </div>

      <el-menu
        :default-active="activeMenu"
        class="el-menu-vertical"
        background-color="#00B51D"
        text-color="#fff"
        active-text-color="#ffd04b"
        router
      >
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
        <el-menu-item index="/login">
          <el-icon><SwitchButton /></el-icon>
          <span>退出登录</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item>首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ pageTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <span class="user-badge">👤 用户 ID: {{ userId }}</span>
        </div>
      </el-header>

      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import { Film, Menu, DataAnalysis, ChatLineRound, SwitchButton } from '@element-plus/icons-vue';

const route = useRoute();
const userId = ref(localStorage.getItem('currentUserId') || '1');
const activeMenu = computed(() => route.path);
const pageTitle = computed(() => {
  const maps = { '/recommend': '个性化推荐', '/analysis': '数据统计', '/insight': '评论洞察' };
  return maps[route.path] || '欢迎使用';
});
</script>

<style scoped>
.layout-container { height: 100vh; overflow: hidden; }
.aside { background-color: #00B51D; transition: width 0.3s; box-shadow: 2px 0 10px rgba(0,0,0,0.1); }
.logo { height: 60px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; border-bottom: 1px solid rgba(255,255,255,0.1); }
.logo span { margin-left: 10px; font-size: 16px; }
.el-menu { border-right: none; }
.header { background: #fff; border-bottom: 1px solid #eee; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; }
.user-badge { font-size: 14px; color: #666; background: #f5f7fa; padding: 5px 15px; border-radius: 20px; }
.main-content { background-color: #f0f2f5; padding: 20px; overflow-y: auto; }
</style>