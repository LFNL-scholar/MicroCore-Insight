<template>
  <div class="device-card">
    <div :class="['status-bar', isOnline ? 'online' : 'offline']"></div>
    <div class="card-content">
      <div class="card-header">
        <h3 class="device-name">{{ deviceName }}</h3>
        <span :class="['status-text', isOnline ? 'online' : 'offline']">
          {{ isOnline ? '在线' : '离线' }}
        </span>
      </div>
      <div class="device-info">
        <div class="info-item">
          <span class="label">设备ID:</span>
          <span class="value">{{ deviceId }}</span>
        </div>
        <div class="info-item">
          <span class="label">Mac地址:</span>
          <span class="value">{{ macAddress }}</span>
        </div>
        <div class="info-item">
          <span class="label">最近活跃:</span>
          <span class="value" :class="{ 'active-now': isOnline }">
            {{ isOnline ? '正在活跃' : lastActive }}
          </span>
        </div>
      </div>
      <div class="card-actions">
        <button class="action-btn" @click="showEditNameDialog = true">修改昵称</button>
        <button class="action-btn" @click="$emit('config-role', deviceId)">配置角色</button>
        <button class="action-btn" @click="$emit('view-history', deviceId)">历史对话</button>
        <button class="action-btn" @click="handleViewDetail">详细信息</button>
      </div>
    </div>

    <!-- 修改昵称对话框 -->
    <EditDeviceNameDialog
      v-model="showEditNameDialog"
      :current-name="deviceName"
      @confirm="handleEditName"
    />
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import EditDeviceNameDialog from './EditDeviceNameDialog.vue'

export default {
  name: 'DeviceCard',
  components: {
    EditDeviceNameDialog
  },
  props: {
    deviceId: {
      type: [String, Number],
      required: true
    },
    deviceName: {
      type: String,
      default: '未命名设备'
    },
    macAddress: {
      type: String,
      required: true
    },
    lastActive: {
      type: String,
      required: true
    },
    isOnline: {
      type: Boolean,
      default: false
    }
  },
  emits: ['config-role', 'view-history', 'update-name'],
  setup(props, { emit }) {
    const router = useRouter()
    const showEditNameDialog = ref(false)

    const handleViewDetail = () => {
      router.push(`/device/${props.deviceId}`)
    }

    const handleEditName = async (newName) => {
      try {
        // 触发更新昵称事件
        await emit('update-name', {
          deviceId: props.deviceId,
          newName: newName
        })
        return true
      } catch (error) {
        throw error
      }
    }

    return {
      showEditNameDialog,
      handleEditName,
      handleViewDetail
    }
  }
}
</script>

<style scoped>
.device-card {
  display: flex;
  background: white;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
  min-width: 320px;
}

.status-bar {
  width: 4px;
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
}

.status-bar.online {
  background-color: #4caf50;
}

.status-bar.offline {
  background-color: #f44336;
}

.card-content {
  flex: 1;
  padding: 0.75rem 1rem;
  padding-left: calc(1rem + 4px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
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
  margin-bottom: 0.75rem;
}

.info-item {
  display: flex;
  margin-bottom: 0.25rem;
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

.info-item .value.active-now {
  color: #4caf50;
  font-weight: 500;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: space-between;
  width: 100%;
}

.action-btn {
  padding: 0.35rem 0.5rem;
  border: 1px solid #313a7e;
  border-radius: 4px;
  background: white;
  color: #313a7e;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.8rem;
  white-space: nowrap;
  flex: 1;
  text-align: center;
  min-width: 0;
}

.action-btn:hover {
  background: #313a7e;
  color: white;
}

@media (max-width: 768px) {
  .info-item {
    flex-direction: column;
  }

  .info-item .label {
    width: auto;
    margin-bottom: 0.25rem;
  }

  .card-actions {
    flex-wrap: wrap;
  }

  .action-btn {
    flex: 1 1 calc(50% - 0.25rem);
  }
}
</style> 