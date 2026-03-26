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
import axios from 'axios';

const router = useRouter();
const activeTab = ref('login');
const loading = ref(false);

const loginForm = ref({ username: '', password: '' });
const regForm = ref({ username: '', password: '' });

// 统一处理登录和注册
const handleAuth = async (action) => {
  const isLogin = action === 'login';
  const form = isLogin ? loginForm.value : regForm.value;

  if (!form.username || !form.password) {
    ElMessage.warning('账号和密码不能为空！');
    return;
  }

  loading.value = true;
  try {
    const url = isLogin ? 'http://127.0.0.1:5000/api/login' : 'http://127.0.0.1:5000/api/register';
    const res = await axios.post(url, form);

    ElMessage.success(res.data.message);

    // 如果是登录成功，把 user_id 存到本地，然后跳转到推荐首页
    if (isLogin) {
      localStorage.setItem('currentUserId', res.data.user_id);
      localStorage.setItem('currentUserName', res.data.username);
      router.push('/recommend');
    } else {
      // 注册成功后自动切回登录页面
      activeTab.value = 'login';
      loginForm.value.username = regForm.value.username;
    }
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '网络请求失败，请检查后端是否启动');
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
  background-image: url('https://picsum.photos/1920/1080?blur=5'); /* 电影感模糊背景 */
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
  color: #00B51D; /* 豆瓣绿 */
  margin-bottom: 20px;
}
.submit-btn {
  width: 100%;
  margin-top: 10px;
}
</style>