<template>
  <div class="console-container">
    <div class="header-actions">
      <button class="add-device-btn" @click="handleAddDevice">
        <span class="plus-icon">+</span>
        添加设备
      </button>
    </div>
    
    <div class="device-grid">
      <!-- 在线设备卡片 -->
      <div class="device-card">
        <div class="status-bar online"></div>
        <div class="card-content">
          <div class="card-header">
            <h3 class="device-name">设备昵称</h3>
            <span class="status-text online">在线</span>
          </div>
          <div class="device-info">
            <div class="info-item">
              <span class="label">设备ID:</span>
              <span class="value">3940</span>
            </div>
            <div class="info-item">
              <span class="label">Mac地址:</span>
              <span class="value">48:ca:43:e7:29:40</span>
            </div>
            <div class="info-item">
              <span class="label">最近活跃:</span>
              <span class="value">2025-04-01 21:52:14</span>
            </div>
          </div>
          <div class="card-actions">
            <button class="action-btn" @click="handleConfigRole(3940)">配置角色</button>
            <button class="action-btn" @click="handleViewHistory(3940)">历史对话</button>
          </div>
        </div>
      </div>

      <!-- 离线设备卡片 -->
      <div class="device-card">
        <div class="status-bar offline"></div>
        <div class="card-content">
          <div class="card-header">
            <h3 class="device-name">设备昵称2</h3>
            <span class="status-text offline">离线</span>
          </div>
          <div class="device-info">
            <div class="info-item">
              <span class="label">设备ID:</span>
              <span class="value">3941</span>
            </div>
            <div class="info-item">
              <span class="label">Mac地址:</span>
              <span class="value">48:ca:43:e7:29:41</span>
            </div>
            <div class="info-item">
              <span class="label">最近活跃:</span>
              <span class="value">2025-04-01 20:30:00</span>
            </div>
          </div>
          <div class="card-actions">
            <button class="action-btn" @click="handleConfigRole(3941)">配置角色</button>
            <button class="action-btn" @click="handleViewHistory(3941)">历史对话</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'ConsolePage',
  setup() {
    const router = useRouter()

    const handleAddDevice = () => {
      // 处理添加设备的逻辑
      console.log('添加设备')
    }

    const handleConfigRole = (deviceId) => {
      router.push(`/role-config/${deviceId}`)
    }

    const handleViewHistory = (deviceId) => {
      // 处理查看历史对话的逻辑
      console.log('查看历史对话', deviceId)
    }

    return {
      handleAddDevice,
      handleConfigRole,
      handleViewHistory
    }
  }
}
</script>

<style scoped>
.console-container {
  padding: 1.5rem;
}

.header-actions {
  margin-bottom: 1.5rem;
}

.add-device-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #313a7e;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.add-device-btn:hover {
  background-color: #252d63;
}

.plus-icon {
  font-size: 1rem;
  font-weight: bold;
}

.device-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.device-card {
  display: flex;
  background: white;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.status-bar {
  width: 6px;
}

.status-bar.online {
  background-color: #4caf50;
}

.status-bar.offline {
  background-color: #f44336;
}

.card-content {
  flex: 1;
  padding: 1rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.device-name {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
}

.status-text {
  font-size: 0.8rem;
  padding: 0.2rem 0.6rem;
  border-radius: 10px;
}

.status-text.online {
  background-color: #e8f5e9;
  color: #4caf50;
}

.status-text.offline {
  background-color: #ffebee;
  color: #f44336;
}

.device-info {
  margin-bottom: 1rem;
}

.info-item {
  display: flex;
  margin-bottom: 0.4rem;
  font-size: 0.9rem;
}

.info-item .label {
  color: #666;
  width: 80px;
  flex-shrink: 0;
}

.info-item .value {
  color: #333;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-start;
}

.action-btn {
  padding: 0.35rem 0.75rem;
  border: 1px solid #313a7e;
  border-radius: 4px;
  background: white;
  color: #313a7e;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.85rem;
  flex: 0 1 auto;
  white-space: nowrap;
}

.action-btn:hover {
  background: #313a7e;
  color: white;
}

@media (max-width: 768px) {
  .console-container {
    padding: 1rem;
  }

  .device-grid {
    grid-template-columns: 1fr;
  }

  .info-item {
    flex-direction: column;
  }

  .info-item .label {
    width: auto;
    margin-bottom: 0.25rem;
  }
}
</style> 