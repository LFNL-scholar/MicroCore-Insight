<template>
  <div class="register-container">
    <div class="register-box">
      <h2>注册账号</h2>
      <form @submit.prevent="handleRegister" class="register-form">
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
        <div class="form-group">
          <input
            type="password"
            v-model="confirmPassword"
            placeholder="确认密码"
            required
            :disabled="isLoading"
          />
        </div>
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
        <button type="submit" class="register-button" :disabled="isLoading">
          {{ isLoading ? '注册中...' : '注册' }}
        </button>
      </form>
      <div class="login-link">
        已有账号？
        <router-link to="/login">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '../api/auth'

export default {
  name: 'RegisterPage',
  setup() {
    const router = useRouter()
    const userId = ref('')
    const password = ref('')
    const confirmPassword = ref('')
    const errorMessage = ref('')
    const isLoading = ref(false)

    const handleRegister = async () => {
      if (isLoading.value) return

      // 表单验证
      if (password.value !== confirmPassword.value) {
        errorMessage.value = '两次输入的密码不一致'
        return
      }

      if (password.value.length < 6) {
        errorMessage.value = '密码长度不能少于6位'
        return
      }

      console.log('开始注册流程')
      console.log('用户ID:', userId.value)
      
      errorMessage.value = ''
      isLoading.value = true

      try {
        console.log('发送注册请求...')
        const response = await register(userId.value, password.value)
        console.log('注册响应:', response)

        if (response.status === 'success') {
          console.log('注册成功，即将跳转到登录页')
          // 显示成功消息
          alert('注册成功！请登录')
          // 跳转到登录页
          router.push('/login')
        }
      } catch (error) {
        console.error('注册失败:', error)
        errorMessage.value = error.message || '注册失败，请稍后重试'
      } finally {
        console.log('注册流程结束')
        isLoading.value = false
      }
    }

    return {
      userId,
      password,
      confirmPassword,
      errorMessage,
      isLoading,
      handleRegister
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.register-box {
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

.register-form {
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

input:disabled {
  background-color: #e9ecef;
  cursor: not-allowed;
}

.register-button {
  background-color: #313a7e;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.register-button:hover {
  background-color: #252d63;
}

.register-button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  margin-top: 1rem;
}

.login-link a {
  color: #313a7e;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}

.error-message {
  color: #dc3545;
  font-size: 0.875rem;
  margin-bottom: 1rem;
  text-align: center;
}
</style> 