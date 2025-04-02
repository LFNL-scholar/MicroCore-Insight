<template>
  <div class="settings-container">
    <div class="settings-content">
      <h1>账号设置</h1>
      
      <div class="tabs">
        <div 
          class="tab" 
          :class="{ active: activeTab === 'basic' }"
          @click="activeTab = 'basic'"
        >
          基本信息
        </div>
        <div 
          class="tab" 
          :class="{ active: activeTab === 'password' }"
          @click="activeTab = 'password'"
        >
          修改密码
        </div>
        <div 
          class="tab" 
          :class="{ active: activeTab === 'delete' }"
          @click="activeTab = 'delete'"
        >
          删除账号
        </div>
      </div>

      <div class="tab-content">
        <!-- 基本信息 -->
        <div v-show="activeTab === 'basic'" class="tab-pane">
          <div class="form-group">
            <label>账号名</label>
            <input type="text" v-model="accountName" disabled />
          </div>
          <div class="form-group">
            <label>昵称</label>
            <input type="text" v-model="nickname" placeholder="请输入昵称" />
          </div>
          <div class="form-group">
            <label>邮箱</label>
            <input type="email" v-model="email" placeholder="请输入邮箱" />
          </div>
          <div class="form-group">
            <label>手机号</label>
            <input type="tel" v-model="phone" placeholder="请输入手机号" />
          </div>
          <button class="save-button" @click="saveBasicInfo">保存修改</button>
        </div>

        <!-- 修改密码 -->
        <div v-show="activeTab === 'password'" class="tab-pane">
          <div class="form-group">
            <label>新密码</label>
            <input type="password" v-model="newPassword" placeholder="请输入新密码" />
          </div>
          <div class="form-group">
            <label>确认密码</label>
            <input type="password" v-model="confirmPassword" placeholder="请再次输入新密码" />
          </div>
          <button class="save-button" @click="updatePassword">更新密码</button>
        </div>

        <!-- 删除账号 -->
        <div v-show="activeTab === 'delete'" class="tab-pane danger-zone">
          <p class="warning-text">警告：此操作不可逆，账号删除后将无法恢复</p>
          <div class="form-group">
            <label>请输入密码确认删除</label>
            <input 
              type="password" 
              v-model="deletePassword" 
              placeholder="请输入密码" 
              :disabled="isDeleting"
            />
          </div>
          <div v-if="deleteError" class="error-message">
            {{ deleteError }}
          </div>
          <button 
            class="delete-button" 
            @click="confirmDeleteAccount"
            :disabled="isDeleting"
          >
            {{ isDeleting ? '删除中...' : '删除账号' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { deleteUser } from '../api/auth'

export default {
  name: 'SettingsPage',
  setup() {
    const router = useRouter()
    const activeTab = ref('basic')
    
    // 基本信息
    const accountName = ref(localStorage.getItem('userId') || '')
    const nickname = ref('小云')
    const email = ref('example@email.com')
    const phone = ref('+86185****7311')

    // 密码修改
    const newPassword = ref('')
    const confirmPassword = ref('')

    // 删除账号
    const deletePassword = ref('')
    const deleteError = ref('')
    const isDeleting = ref(false)

    const saveBasicInfo = async () => {
      try {
        // 这里添加保存基本信息的逻辑
        alert('基本信息保存成功')
      } catch (error) {
        alert('保存失败：' + error.message)
      }
    }

    const updatePassword = async () => {
      if (newPassword.value !== confirmPassword.value) {
        alert('两次输入的密码不一致')
        return
      }
      if (newPassword.value.length < 6) {
        alert('密码长度不能少于6位')
        return
      }
      try {
        // 这里添加更新密码的逻辑
        alert('密码更新成功')
        newPassword.value = ''
        confirmPassword.value = ''
      } catch (error) {
        alert('密码更新失败：' + error.message)
      }
    }

    const confirmDeleteAccount = async () => {
      if (!deletePassword.value) {
        deleteError.value = '请输入密码'
        return
      }

      if (!confirm('确定要删除账号吗？此操作不可恢复！')) {
        return
      }

      console.log('开始删除账号流程')
      isDeleting.value = true
      deleteError.value = ''

      try {
        console.log('发送删除账号请求...')
        const response = await deleteUser(accountName.value, deletePassword.value)
        console.log('删除响应:', response)

        if (response.status === 'success') {
          console.log('账号删除成功，即将退出登录')
          // 清除本地存储的用户信息
          localStorage.removeItem('userId')
          // 显示成功消息
          alert('账号已成功删除')
          // 跳转到登录页
          router.push('/login')
        }
      } catch (error) {
        console.error('删除失败:', error)
        deleteError.value = error.message || '删除失败，请稍后重试'
      } finally {
        console.log('删除账号流程结束')
        isDeleting.value = false
      }
    }

    return {
      activeTab,
      accountName,
      nickname,
      email,
      phone,
      newPassword,
      confirmPassword,
      deletePassword,
      deleteError,
      isDeleting,
      saveBasicInfo,
      updatePassword,
      confirmDeleteAccount
    }
  }
}
</script>

<style scoped>
.settings-container {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.settings-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  color: #313a7e;
  margin-bottom: 2rem;
}

.tabs {
  display: flex;
  border-bottom: 2px solid #eee;
  margin-bottom: 2rem;
}

.tab {
  padding: 1rem 2rem;
  cursor: pointer;
  color: #666;
  font-weight: 500;
  position: relative;
}

.tab.active {
  color: #313a7e;
}

.tab.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #313a7e;
}

.tab-content {
  padding: 1rem 0;
}

.tab-pane {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
  color: #666;
}

input:focus {
  outline: none;
  border-color: #313a7e;
}

input::placeholder {
  color: #999;
}

.save-button {
  background-color: #313a7e;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 1rem;
  width: fit-content;
}

.save-button:hover {
  background-color: #252d63;
}

.danger-zone {
  background-color: #fff8f8;
  padding: 1.5rem;
  border-radius: 4px;
}

.warning-text {
  color: #dc3545;
  margin-bottom: 1rem;
}

.error-message {
  color: #dc3545;
  font-size: 0.875rem;
  margin: 0.5rem 0;
}

.delete-button {
  background-color: #dc3545;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
  width: 100%;
  margin-top: 1rem;
}

.delete-button:hover {
  background-color: #c82333;
}

.delete-button:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}
</style> 