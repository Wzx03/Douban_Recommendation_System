<template>
  <div class="login-container">
    <el-card class="login-card" shadow="always">
      <div class="logo-title">豆瓣电影推荐系统</div>
      <el-tabs v-model="activeTab">
        <el-tab-pane label="登录" name="login">
          <el-form :model="loginForm" @keyup.enter="handleAuth('login')">
            <el-form-item>
              <el-input v-model="loginForm.username" placeholder="请输入用户名" prefix-icon="User" />
            </el-form-item>
            <el-form-item>
              <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" prefix-icon="Lock" show-password />
            </el-form-item>
            <el-button type="primary" class="submit-btn" :loading="loading" @click="handleAuth('login')">登 录</el-button>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="注册" name="register">
          <el-form :model="regForm">
            <el-form-item>
              <el-input v-model="regForm.username" placeholder="设置用户名" prefix-icon="User" />
            </el-form-item>
            <el-form-item>
              <el-input v-model="regForm.password" type="password" placeholder="设置密码" prefix-icon="Lock" show-password />
            </el-form-item>
            <el-button type="success" class="submit-btn" :loading="loading" @click="handleAuth('register')">注 册</el-button>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { reqLogin, reqRegister } from '@/api/index.js'; // 🌟 使用统一 API 接口

const router = useRouter();
const activeTab = ref('login');
const loading = ref(false);

const loginForm = ref({ username: '', password: '' });
const regForm = ref({ username: '', password: '' });

const handleAuth = async (action) => {
  const isLogin = action === 'login';
  const form = isLogin ? loginForm.value : regForm.value;

  if (!form.username || !form.password) {
    ElMessage.warning('账号和密码不能为空！');
    return;
  }

  loading.value = true;
  try {
    if (isLogin) {
      const res = await reqLogin(form); // 🌟 调用 API
      localStorage.setItem('currentUserId', res.user_id);
      localStorage.setItem('currentUserName', res.username);
      ElMessage.success('登录成功！');
      router.push('/recommend');
    } else {
      const res = await reqRegister(form); // 🌟 调用 API
      ElMessage.success(`注册成功！您的用户ID为：${res.user_id}，请登录`);
      activeTab.value = 'login';
      loginForm.value.username = regForm.value.username;
    }
  } catch (err) {
    // 兼容拦截器脱壳后的报错信息
    ElMessage.error(err.response?.data?.detail || err.message || '操作失败');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f3f5;
  background-image: url('https://picsum.photos/1920/1080?blur=5');
  background-size: cover;
}
.login-card {
  width: 400px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.95);
}
.logo-title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  color: #00B51D;
  margin-bottom: 20px;
}
.submit-btn {
  width: 100%;
  margin-top: 10px;
}
</style>