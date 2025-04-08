<template>
  <div class="role-config-container">
    <div class="header">
      <button class="back-btn" @click="handleBack">
        <span class="arrow">←</span>
        返回
      </button>
      <h2 class="page-title">配置角色</h2>
    </div>
    <div class="form-container">
      <div v-if="isLoading" class="loading-state">
        加载中...
      </div>
      <div v-else-if="error" class="error-message">
        {{ error }}
        <button class="retry-button" @click="loadVoiceList">重试</button>
      </div>
      <template v-else>
        <div class="template-section">
          <button class="template-btn" @click="useDefaultTemplate">
            <span class="template-icon">📋</span>
            默认模板
          </button>
        </div>
        <div class="form-group">
          <label>角色昵称</label>
          <input 
            type="text" 
            v-model="roleName" 
            placeholder="请输入角色昵称"
            class="input-field"
          >
        </div>
        <div class="form-group">
          <label>角色音色</label>
          <select 
            v-model="selectedVoice" 
            class="input-field select-field"
          >
            <option value="" disabled>请选择音色</option>
            <option 
              v-for="voice in voiceList" 
              :key="voice" 
              :value="voice"
            >
              {{ voice }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label>角色介绍</label>
          <textarea 
            v-model="roleDescription" 
            placeholder="我是一个叫{name}的智能助手，可以陪你聊天，帮助你回答各种问题。"
            class="input-field textarea"
            rows="6"
          ></textarea>
        </div>
        <div class="button-group">
          <button class="reset-btn" @click="handleReset" :disabled="isSaving">重置</button>
          <button 
            class="save-btn" 
            @click="handleSave"
            :disabled="!isFormValid || isSaving"
          >
            {{ isSaving ? '保存中...' : '保存' }}
          </button>
        </div>
        <div v-if="saveError" class="save-error">
          {{ saveError }}
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getVoiceList, configureDeviceRole, getDeviceRole } from '../api/device'

export default {
  name: 'RoleConfigPage',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const deviceId = route.params.deviceId

    const roleName = ref('')
    const selectedVoice = ref('')
    const roleDescription = ref('')
    const voiceList = ref([])
    const isLoading = ref(true)
    const error = ref('')
    const isSaving = ref(false)
    const saveError = ref('')

    const isFormValid = computed(() => {
      return roleName.value.trim() && selectedVoice.value && roleDescription.value.trim()
    })

    // 加载角色配置信息
    const loadRoleConfig = async () => {
      try {
        const response = await getDeviceRole(deviceId)
        if (response.status === 'success') {
          roleName.value = response.assistant_name || ''
          selectedVoice.value = response.assistant_voice || ''
          roleDescription.value = response.assistant_prompt || ''
          console.log('角色配置加载成功:', {
            name: roleName.value,
            voice: selectedVoice.value,
            description: roleDescription.value
          })
        } else if (response.status === 'not_found') {
          // 如果角色信息不存在，显示提示信息但不影响表单使用
          console.log('角色信息不存在，使用空表单')
          // 在表单上方显示提示信息
          saveError.value = '该设备尚未配置角色信息，请填写配置'
          setTimeout(() => {
            saveError.value = ''  // 3秒后清除提示
          }, 3000)
        } else {
          throw new Error(response.message || '获取角色配置失败')
        }
      } catch (err) {
        console.error('加载角色配置失败:', err)
        error.value = err.message || '加载角色配置失败，请稍后重试'
      }
    }

    const loadVoiceList = async () => {
      isLoading.value = true
      error.value = ''

      try {
        console.log('开始加载音色列表...')
        const response = await getVoiceList()
        console.log('音色列表响应:', response)
        
        if (response.status === 'success' && Array.isArray(response.voice_list)) {
          voiceList.value = response.voice_list
          console.log('成功加载音色列表:', voiceList.value)
          // 加载音色列表成功后，加载角色配置
          await loadRoleConfig()
        } else {
          console.error('音色列表格式错误:', response)
          throw new Error('获取音色列表失败：数据格式错误')
        }
      } catch (err) {
        console.error('加载音色列表失败:', err)
        if (err.response?.status === 404) {
          error.value = 'API接口未找到，请确认后端服务是否正常运行'
        } else {
          error.value = err.message || '加载音色列表失败，请稍后重试'
        }
      } finally {
        isLoading.value = false
      }
    }

    const handleBack = () => {
      router.push('/console')
    }

    const handleSave = async () => {
      if (!isFormValid.value || isSaving.value) return

      isSaving.value = true
      saveError.value = ''

      try {
        const response = await configureDeviceRole(
          deviceId,
          roleName.value.trim(),
          selectedVoice.value,
          roleDescription.value.trim()
        )

        if (response.status === 'success') {
          // 保存成功后返回设备列表页面
          router.push('/console')
        }
      } catch (err) {
        console.error('保存角色配置失败:', err)
        saveError.value = err.message || '保存失败，请稍后重试'
      } finally {
        isSaving.value = false
      }
    }

    const handleReset = () => {
      roleName.value = ''
      selectedVoice.value = ''
      roleDescription.value = ''
    }

    const useDefaultTemplate = () => {
      roleName.value = '小云'
      selectedVoice.value = '爽快思思/Skye'
      roleDescription.value = '我是一个叫{name}的女孩，声音好听，习惯简短表达。梦想是帮助人们解决生活中的各种问题,逗人们开心。'
    }

    onMounted(() => {
      loadVoiceList()
    })

    return {
      roleName,
      selectedVoice,
      roleDescription,
      voiceList,
      isLoading,
      error,
      isSaving,
      saveError,
      isFormValid,
      handleSave,
      handleReset,
      handleBack,
      loadVoiceList,
      useDefaultTemplate
    }
  }
}
</script>

<style scoped>
.role-config-container {
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

.form-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
  animation: fadeIn 0.3s ease-out;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-size: 0.9rem;
}

.input-field {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
  transition: border-color 0.2s;
}

.input-field:focus {
  outline: none;
  border-color: #313a7e;
}

.textarea {
  resize: vertical;
  min-height: 120px;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.save-btn, .reset-btn {
  padding: 0.75rem 2rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.save-btn {
  background-color: #313a7e;
  color: white;
  border: none;
}

.save-btn:hover {
  background-color: #252d63;
}

.reset-btn {
  background-color: white;
  color: #666;
  border: 1px solid #ddd;
}

.reset-btn:hover {
  background-color: #f5f5f5;
}

@media (max-width: 768px) {
  .role-config-container {
    padding: 1rem;
  }

  .form-container {
    padding: 1.5rem;
  }

  .button-group {
    flex-direction: column-reverse;
  }

  .save-btn, .reset-btn {
    width: 100%;
  }
}

.select-field {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12' fill='none'%3E%3Cpath d='M2.5 4L6 7.5L9.5 4' stroke='%23666666' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 12px;
  padding-right: 2.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.select-field:hover {
  border-color: #313a7e;
}

.select-field:focus {
  border-color: #313a7e;
  box-shadow: 0 0 0 2px rgba(49, 58, 126, 0.1);
}

.select-field option {
  padding: 0.75rem;
  font-size: 0.9rem;
  color: #333;
  background-color: white;
}

.select-field option:hover {
  background-color: #f5f7ff;
}

.select-field:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
  color: #999;
}

/* 添加一个淡入动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.loading-state {
  text-align: center;
  padding: 2rem;
  color: #666;
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

.save-error {
  color: #dc3545;
  text-align: center;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.save-btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
  background-color: #6c757d;
}

.template-section {
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: flex-start;
}

.template-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  color: #666;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.template-btn:hover {
  background-color: #f5f5f5;
  border-color: #313a7e;
  color: #313a7e;
}

.template-icon {
  font-size: 1.1rem;
}
</style> 