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
          <div v-if="isLoading" class="loading-state">
            加载中...
          </div>
          <div v-else-if="loadError" class="error-message">
            {{ loadError }}
            <button class="retry-button" @click="loadUserInfo">重试</button>
          </div>
          <template v-else>
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
          </template>
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { deleteUser } from '../api/auth'
import { getUserInfo, updateUserInfo } from '../api/user'

export default {
  name: 'SettingsPage',
  setup() {
    const router = useRouter()
    const activeTab = ref('basic')
    
    // 基本信息
    const accountName = ref(localStorage.getItem('userId') || '')
    const nickname = ref('')
    const email = ref('')
    const phone = ref('')
    const isLoading = ref(false)
    const loadError = ref('')

    // 加载用户信息
    const loadUserInfo = async () => {
      if (!accountName.value) {
        loadError.value = '用户ID不存在，请重新登录'
        return
      }

      isLoading.value = true
      loadError.value = ''

      try {
        console.log('开始加载用户信息:', accountName.value)
        const response = await getUserInfo(accountName.value)
        console.log('用户信息加载成功:', response)

        // 确保数据存在并赋值
        if (response && response.status === 'success') {
          nickname.value = response.nickname || ''
          email.value = response.email || ''
          phone.value = response.phone ? response.phone.toString() : ''
          
          // 打印赋值后的数据，用于调试
          console.log('更新后的用户信息:', {
            nickname: nickname.value,
            email: email.value,
            phone: phone.value
          })
        } else {
          throw new Error('获取用户信息失败：返回数据格式不正确')
        }
      } catch (error) {
        console.error('加载用户信息失败:', error)
        loadError.value = error.message || '加载用户信息失败，请稍后重试'
        if (error.status === 401) {
          // 如果是未授权，跳转到登录页
          router.push('/login')
        }
      } finally {
        isLoading.value = false
      }
    }

    // 在组件挂载时加载用户信息
    onMounted(() => {
      loadUserInfo()
    })

    // 密码修改
    const newPassword = ref('')
    const confirmPassword = ref('')

    // 删除账号
    const deletePassword = ref('')
    const deleteError = ref('')
    const isDeleting = ref(false)

    const saveBasicInfo = async () => {
      try {
        // 表单验证
        if (!nickname.value.trim()) {
          alert('昵称不能为空')
          return
        }
        if (!email.value.trim()) {
          alert('邮箱不能为空')
          return
        }
        if (!phone.value.trim()) {
          alert('手机号不能为空')
          return
        }

        // 显示加载状态
        isLoading.value = true

        // 准备更新数据
        const updateData = {
          user_id: accountName.value,
          nickname: nickname.value.trim(),
          email: email.value.trim(),
          phone: phone.value.trim()
        }

        console.log('准备更新用户信息:', updateData)
        const response = await updateUserInfo(updateData)
        
        if (response.status === 'success') {
          alert('基本信息保存成功')
          // 重新加载用户信息以确保数据同步
          await loadUserInfo()
        } else {
          throw new Error(response.message || '更新失败')
        }
      } catch (error) {
        console.error('保存失败:', error)
        alert('保存失败：' + (error.message || '请稍后重试'))
      } finally {
        isLoading.value = false
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
          localStorage.clear()
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
      isLoading,
      loadError,
      saveBasicInfo,
      updatePassword,
      confirmDeleteAccount,
      loadUserInfo
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

.loading-state {
  text-align: center;
  color: #666;
  font-size: 1rem;
  margin: 1rem 0;
}

.retry-button {
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

.retry-button:hover {
  background-color: #252d63;
}
</style> 