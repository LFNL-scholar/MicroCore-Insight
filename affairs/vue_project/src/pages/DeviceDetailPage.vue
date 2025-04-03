<template>
  <div class="device-detail-container">
    <div class="header">
      <button class="back-btn" @click="handleBack">
        <span class="arrow">←</span>
        返回
      </button>
      <h2 class="page-title">设备详情</h2>
    </div>

    <div v-if="isLoading" class="loading-state">
      加载中...
    </div>
    <div v-else-if="error" class="error-message">
      {{ error }}
      <button class="retry-button" @click="loadDeviceDetail">重试</button>
    </div>
    <div v-else class="detail-content">
      <div class="detail-card">
        <div class="detail-header">
          <h3 class="device-name">{{ deviceInfo.device_name || '未命名设备' }}</h3>
        </div>

        <div class="detail-section">
          <div class="info-grid">
            <div class="info-item">
              <span class="label">设备ID</span>
              <span class="value">{{ deviceInfo.device_id }}</span>
            </div>
            <div class="info-item">
              <span class="label">MAC地址</span>
              <span class="value">{{ deviceInfo.mac_address }}</span>
            </div>
            <div class="info-item">
              <span class="label">创建于</span>
              <span class="value">{{ deviceInfo.created_at }}</span>
            </div>
            <div class="info-item">
              <span class="label">更新于</span>
              <span class="value">{{ deviceInfo.updated_at === 'None' ? '未更新' : deviceInfo.updated_at }}</span>
            </div>
          </div>
        </div>

        <div class="actions-section">
          <button class="delete-btn" @click="showDeleteConfirm = true">
            删除设备
          </button>
        </div>
      </div>
    </div>

    <!-- 删除确认对话框 -->
    <div v-if="showDeleteConfirm" class="dialog-overlay" @click="showDeleteConfirm = false">
      <div class="dialog-content" @click.stop>
        <div class="dialog-header">
          <h3>删除确认</h3>
          <button class="close-btn" @click="showDeleteConfirm = false">×</button>
        </div>
        <div class="dialog-body">
          <p class="warning-text">确定要删除该设备吗？此操作不可恢复！</p>
          <div v-if="deleteError" class="error-message">{{ deleteError }}</div>
        </div>
        <div class="dialog-footer">
          <button 
            class="cancel-btn" 
            @click="showDeleteConfirm = false"
            :disabled="isDeleting"
          >
            取消
          </button>
          <button 
            class="confirm-btn" 
            @click="handleDelete"
            :disabled="isDeleting"
          >
            {{ isDeleting ? '删除中...' : '确认删除' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getDeviceDetail, deleteDevice } from '../api/device'

export default {
  name: 'DeviceDetailPage',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const deviceInfo = ref({})
    const isLoading = ref(true)
    const error = ref('')
    const showDeleteConfirm = ref(false)
    const isDeleting = ref(false)
    const deleteError = ref('')

    const loadDeviceDetail = async () => {
      const deviceId = route.params.deviceId
      const userId = localStorage.getItem('userId')
      
      if (!deviceId) {
        error.value = '设备ID不存在'
        return
      }

      if (!userId) {
        error.value = '用户未登录，请重新登录'
        router.push('/login')
        return
      }

      isLoading.value = true
      error.value = ''

      try {
        const response = await getDeviceDetail(deviceId, userId)
        if (response.status === 'success') {
          deviceInfo.value = {
            device_name: response.device_name,
            device_id: response.device_id,
            mac_address: response.mac_address,
            created_at: response.created_at,
            updated_at: response.updated_at
          }
        } else {
          throw new Error(response.message || '获取设备详情失败')
        }
      } catch (err) {
        console.error('加载设备详情失败:', err)
        error.value = err.message || '加载设备详情失败，请稍后重试'
        if (err.message === '设备不存在') {
          // 如果设备不存在，3秒后返回设备列表页面
          setTimeout(() => {
            router.push('/console')
          }, 3000)
        }
      } finally {
        isLoading.value = false
      }
    }

    const handleDelete = async () => {
      const userId = localStorage.getItem('userId')
      if (!userId) {
        deleteError.value = '用户未登录，请重新登录'
        return
      }

      isDeleting.value = true
      deleteError.value = ''

      try {
        await deleteDevice(userId, deviceInfo.value.mac_address)
        // 删除成功后返回设备列表页面
        router.push('/console')
      } catch (err) {
        console.error('删除设备失败:', err)
        deleteError.value = err.message || '删除设备失败，请稍后重试'
        if (err.message === '设备不存在') {
          // 如果设备不存在，3秒后返回设备列表页面
          setTimeout(() => {
            router.push('/console')
          }, 3000)
        }
      } finally {
        isDeleting.value = false
      }
    }

    const handleBack = () => {
      router.push('/console')
    }

    onMounted(() => {
      loadDeviceDetail()
    })

    return {
      deviceInfo,
      isLoading,
      error,
      showDeleteConfirm,
      isDeleting,
      deleteError,
      handleBack,
      handleDelete,
      loadDeviceDetail
    }
  }
}
</script>

<style scoped>
.device-detail-container {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  background: none;
  color: #666;
  cursor: pointer;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.back-btn:hover {
  color: #313a7e;
}

.arrow {
  font-size: 1.2rem;
}

.page-title {
  color: #333;
  font-size: 1.5rem;
  margin: 0;
}

.detail-content {
  margin-top: 1rem;
}

.detail-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.device-name {
  margin: 0;
  font-size: 1.25rem;
  color: #333;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item .label {
  color: #666;
  font-size: 0.9rem;
}

.info-item .value {
  color: #333;
  font-size: 1rem;
}

.actions-section {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.delete-btn:hover {
  background-color: #c82333;
}

/* 对话框样式 */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
}

.dialog-header {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dialog-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.1rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #666;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.dialog-body {
  padding: 1.5rem;
}

.warning-text {
  color: #dc3545;
  margin: 0;
  text-align: center;
}

.dialog-footer {
  padding: 1rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.cancel-btn, .confirm-btn {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.cancel-btn {
  background-color: white;
  border: 1px solid #ddd;
  color: #666;
}

.cancel-btn:hover {
  background-color: #f5f5f5;
}

.confirm-btn {
  background-color: #dc3545;
  color: white;
  border: none;
}

.confirm-btn:hover:not(:disabled) {
  background-color: #c82333;
}

.cancel-btn:disabled,
.confirm-btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.error-message {
  color: #dc3545;
  text-align: center;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loading-state {
  text-align: center;
  color: #666;
  padding: 2rem;
}

.retry-button {
  background-color: #313a7e;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.retry-button:hover {
  background-color: #252d63;
}

@media (max-width: 768px) {
  .device-detail-container {
    padding: 1rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style> 