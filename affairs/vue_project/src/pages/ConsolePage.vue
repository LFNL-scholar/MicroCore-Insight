<template>
  <div class="console-container">
    <div class="header-actions">
      <button class="add-device-btn" @click="showAddDialog = true">
        <span class="plus-icon">+</span>
        添加设备
      </button>
    </div>
    
    <div class="device-grid">
      <!-- 使用设备卡片组件 -->
      <DeviceCard
        v-for="device in devices"
        :key="device.deviceId"
        :device-id="device.deviceId"
        :device-name="device.deviceName"
        :mac-address="device.macAddress"
        :last-active="device.lastActive"
        :is-online="device.isOnline"
        @config-role="handleConfigRole"
        @view-history="handleViewHistory"
      />
    </div>

    <!-- 添加设备对话框 -->
    <AddDeviceDialog
      v-model="showAddDialog"
      @confirm="handleAddDeviceConfirm"
    />
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import DeviceCard from '../components/DeviceCard.vue'
import AddDeviceDialog from '../components/AddDeviceDialog.vue'
import { bindDevice } from '../api/device'

export default {
  name: 'ConsolePage',
  components: {
    DeviceCard,
    AddDeviceDialog
  },
  setup() {
    const router = useRouter()
    const showAddDialog = ref(false)
    
    // 模拟设备数据
    const devices = ref([
      {
        deviceId: '3940',
        deviceName: '设备昵称',
        macAddress: '48:ca:43:e7:29:40',
        lastActive: '2025-04-01 21:52:14',
        isOnline: true
      },
      {
        deviceId: '3941',
        deviceName: '设备昵称2',
        macAddress: '48:ca:43:e7:29:41',
        lastActive: '2025-04-01 20:30:00',
        isOnline: false
      }
    ])

    const handleAddDeviceConfirm = async (authCode) => {
      try {
        const userId = localStorage.getItem('userId')
        if (!userId) {
          throw new Error('用户未登录，请重新登录')
        }

        console.log('添加设备，认证码:', authCode)
        const response = await bindDevice(authCode, userId)
        
        if (response.status === 'success') {
          // 添加新设备到列表
          devices.value.unshift({
            deviceId: response.device_id,
            deviceName: '新设备',  // 可以后续允许用户修改设备昵称
            macAddress: response.mac_address,
            lastActive: response.created_at,
            isOnline: true  // 新绑定的设备默认在线
          })
          
          // 显示成功消息
          alert('设备绑定成功')
        }
      } catch (error) {
        console.error('添加设备失败:', error)
        throw new Error(error.message || '添加设备失败，请稍后重试')
      }
    }

    const handleConfigRole = (deviceId) => {
      router.push(`/role-config/${deviceId}`)
    }

    const handleViewHistory = (deviceId) => {
      // 处理查看历史对话的逻辑
      console.log('查看历史对话', deviceId)
    }

    return {
      devices,
      showAddDialog,
      handleAddDeviceConfirm,
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

@media (max-width: 768px) {
  .console-container {
    padding: 1rem;
  }

  .device-grid {
    grid-template-columns: 1fr;
  }
}
</style> 