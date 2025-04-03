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
          <span :class="['status-badge', deviceInfo.status === 1 ? 'online' : 'offline']">
            {{ deviceInfo.status === 1 ? '在线' : '离线' }}
          </span>
        </div>

        <div class="detail-section">
          <h4>基本信息</h4>
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
              <span class="label">最近活跃</span>
              <span class="value">{{ deviceInfo.last_active }}</span>
            </div>
            <div class="info-item">
              <span class="label">创建时间</span>
              <span class="value">{{ deviceInfo.created_at }}</span>
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h4>统计信息</h4>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">对话总数</span>
              <span class="value">{{ deviceInfo.total_conversations || 0 }}</span>
            </div>
            <div class="info-item">
              <span class="label">在线时长</span>
              <span class="value">{{ deviceInfo.total_online_time || '0小时' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getDeviceDetail } from '../api/device'

export default {
  name: 'DeviceDetailPage',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const deviceInfo = ref({})
    const isLoading = ref(true)
    const error = ref('')

    const loadDeviceDetail = async () => {
      const deviceId = route.params.deviceId
      if (!deviceId) {
        error.value = '设备ID不存在'
        return
      }

      isLoading.value = true
      error.value = ''

      try {
        const response = await getDeviceDetail(deviceId)
        if (response.status === 'success') {
          deviceInfo.value = response.data
        } else {
          throw new Error(response.message || '获取设备详情失败')
        }
      } catch (err) {
        console.error('加载设备详情失败:', err)
        error.value = err.message || '加载设备详情失败，请稍后重试'
      } finally {
        isLoading.value = false
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
      handleBack,
      loadDeviceDetail
    }
  }
}
</script>

<style scoped>
.device-detail-container {
  padding: 2rem;
  max-width: 1000px;
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

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.9rem;
}

.status-badge.online {
  background-color: #e8f5e9;
  color: #4caf50;
}

.status-badge.offline {
  background-color: #ffebee;
  color: #f44336;
}

.detail-section {
  margin-bottom: 2rem;
}

.detail-section h4 {
  color: #666;
  margin: 0 0 1rem 0;
  font-size: 1rem;
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

.loading-state {
  text-align: center;
  color: #666;
  padding: 2rem;
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