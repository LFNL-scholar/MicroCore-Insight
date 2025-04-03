<template>
  <div class="console-container">
    <div class="header-actions">
      <button class="add-device-btn" @click="showAddDialog = true">
        <span class="plus-icon">+</span>
        添加设备
      </button>
    </div>
    
    <div v-if="isLoading" class="loading-state">
      加载中...
    </div>
    <div v-else-if="loadError" class="error-message">
      {{ loadError }}
      <button class="retry-button" @click="loadDevices">重试</button>
    </div>
    <div v-else>
      <div v-if="devices.length === 0" class="empty-state">
        暂无设备，请添加设备
      </div>
      <div v-else class="device-grid">
        <DeviceCard
          v-for="device in devices"
          :key="device.device_id"
          :device-id="device.device_id"
          :device-name="device.device_name"
          :mac-address="device.mac_address"
          :last-active="device.last_active"
          :is-online="device.status === 1"
          @config-role="handleConfigRole"
          @view-history="handleViewHistory"
          @update-name="handleUpdateDeviceName"
        />
      </div>
    </div>

    <!-- 添加设备对话框 -->
    <AddDeviceDialog
      v-model="showAddDialog"
      @confirm="handleAddDeviceConfirm"
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import DeviceCard from '../components/DeviceCard.vue'
import AddDeviceDialog from '../components/AddDeviceDialog.vue'
import { bindDevice, getUserDevices, updateDeviceName } from '../api/device'

export default {
  name: 'ConsolePage',
  components: {
    DeviceCard,
    AddDeviceDialog
  },
  setup() {
    const router = useRouter()
    const showAddDialog = ref(false)
    const devices = ref([])
    const isLoading = ref(false)
    const loadError = ref('')
    
    // 加载用户设备列表
    const loadDevices = async () => {
      const userId = localStorage.getItem('userId')
      if (!userId) {
        loadError.value = '用户未登录，请重新登录'
        return
      }

      isLoading.value = true
      loadError.value = ''

      try {
        const response = await getUserDevices(userId)
        if (response.status === 'success') {
          devices.value = response.devices
        }
      } catch (error) {
        console.error('加载设备列表失败:', error)
        loadError.value = error.message || '加载设备列表失败，请稍后重试'
        if (error.message === '用户不存在') {
          router.push('/login')
        }
      } finally {
        isLoading.value = false
      }
    }

    const handleAddDeviceConfirm = async (authCode) => {
      try {
        const userId = localStorage.getItem('userId')
        if (!userId) {
          throw new Error('用户未登录，请重新登录')
        }

        console.log('添加设备，认证码:', authCode)
        const response = await bindDevice(authCode, userId)
        
        if (response.status === 'success') {
          // 重新加载设备列表
          await loadDevices()
          return response
        }
        throw new Error(response.message || '添加设备失败')
      } catch (error) {
        console.error('添加设备失败:', error)
        throw error
      }
    }

    const handleConfigRole = (deviceId) => {
      router.push(`/role-config/${deviceId}`)
    }

    const handleViewHistory = (deviceId) => {
      // 处理查看历史对话的逻辑
      console.log('查看历史对话', deviceId)
    }

    const handleUpdateDeviceName = async ({ deviceId, newName }) => {
      try {
        await updateDeviceName(deviceId, newName)
        // 更新本地设备列表中的设备名称
        const deviceIndex = devices.value.findIndex(d => d.device_id === deviceId)
        if (deviceIndex !== -1) {
          devices.value[deviceIndex].device_name = newName
        }
        return true
      } catch (error) {
        console.error('Failed to update device name:', error)
        throw new Error('更新设备昵称失败，请重试')
      }
    }

    // 组件挂载时加载设备列表
    onMounted(() => {
      loadDevices()
    })

    return {
      devices,
      showAddDialog,
      isLoading,
      loadError,
      handleAddDeviceConfirm,
      handleConfigRole,
      handleViewHistory,
      handleUpdateDeviceName,
      loadDevices
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
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
  padding: 0.5rem;
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

.empty-state {
  text-align: center;
  color: #666;
  padding: 2rem;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .console-container {
    padding: 1rem;
  }

  .device-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
</style> 