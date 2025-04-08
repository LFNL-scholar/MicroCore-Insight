<template>
  <div class="login-container">
    <div class="login-box">
      <h2>端侧AI控制面板</h2>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <input
            type="text"
            v-model="userId"
            placeholder="用户名"
            required
            :disabled="isLoading"
          />
        </div>
        <div class="form-group">
          <input
            type="password"
            v-model="password"
            placeholder="密码"
            required
            :disabled="isLoading"
          />
        </div>
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
        <button type="submit" class="login-button" :disabled="isLoading">
          {{ isLoading ? '登录中...' : '登录' }}
        </button>
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
import { login } from '../api/auth'

export default {
  name: 'LoginPage',
  setup() {
    const router = useRouter()
    const userId = ref('')
    const password = ref('')
    const errorMessage = ref('')
    const isLoading = ref(false)

    const handleLogin = async () => {
      if (isLoading.value) return
      
      errorMessage.value = ''
      isLoading.value = true
      
      try {
        const response = await login(userId.value, password.value)
        
        if (response.status === 'success') {
          // 存储用户信息
          localStorage.setItem('userId', response.user_id)
          // 跳转到首页
          router.push('/home')
        }
      } catch (error) {
        errorMessage.value = error.message || '登录失败，请稍后重试'
      } finally {
        isLoading.value = false
      }
    }

    return {
      userId,
      password,
      errorMessage,
      isLoading,
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

.error-message {
  color: #dc3545;
  font-size: 0.875rem;
  margin-bottom: 1rem;
  text-align: center;
}

.login-button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

input:disabled {
  background-color: #e9ecef;
  cursor: not-allowed;
}
</style>