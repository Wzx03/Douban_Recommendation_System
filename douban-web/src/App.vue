<template>
  <el-container>
    <el-header style="background-color: #00B51D; color: white; line-height: 60px;">
      <span style="font-size: 20px; font-weight: bold;">豆瓣电影推荐系统</span>
      <el-menu mode="horizontal" background-color="#00B51D" text-color="#fff" active-text-color="#ffd04b" style="float: right;" router>
        <el-menu-item index="/recommend">个性化推荐</el-menu-item>
        <el-menu-item index="/analysis">数据分析</el-menu-item>
      </el-menu>
    </el-header>

    <el-main>
      <router-view></router-view>
    </el-main>
  </el-container>
</template>

<style>
body { margin: 0; font-family: Avenir, Helvetica, Arial, sans-serif; }
</style>