<template>
  <div class="login-container">
    <div class="login-box">
      <h2>小智AI控制面板</h2>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <input
            type="text"
            v-model="username"
            placeholder="用户名"
            required
          />
        </div>
        <div class="form-group">
          <input
            type="password"
            v-model="password"
            placeholder="密码"
            required
          />
        </div>
        <button type="submit" class="login-button">登录</button>
      </form>
      <div class="register-link">
        还没有账号？
        <router-link to="/register">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'LoginPage',
  setup() {
    const router = useRouter()
    const username = ref('')
    const password = ref('')

    const handleLogin = async () => {
      // 这里添加登录逻辑
      try {
        // 模拟登录成功
        console.log('登录成功')
        router.push('/home')
      } catch (error) {
        console.error('登录失败:', error)
      }
    }

    return {
      username,
      password,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.login-box {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  color: #313a7e;
  margin-bottom: 2rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: #313a7e;
}

.login-button {
  background-color: #313a7e;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-button:hover {
  background-color: #252d63;
}

.register-link {
  text-align: center;
  margin-top: 1rem;
}

.register-link a {
  color: #313a7e;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}
</style> 