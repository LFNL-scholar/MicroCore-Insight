<template>
  <div v-if="modelValue" class="dialog-overlay" @click="handleOverlayClick">
    <div class="dialog-content" @click.stop>
      <div class="dialog-header">
        <h3>添加设备</h3>
        <button class="close-btn" @click="handleClose">×</button>
      </div>
      <div class="dialog-body">
        <div class="form-group">
          <label>设备认证码</label>
          <input 
            type="text" 
            v-model="authCode"
            placeholder="请输入6位设备认证码"
            :disabled="isLoading"
            maxlength="6"
            @keyup.enter="handleConfirm"
            class="auth-code-input"
            @input="handleInput"
          />
          <div v-if="errorMessage" class="error-message">
            <span class="error-icon">!</span>
            {{ errorMessage }}
          </div>
          <div v-if="successMessage" class="success-message">
            <span class="success-icon">✓</span>
            {{ successMessage }}
          </div>
        </div>
      </div>
      <div class="dialog-footer">
        <button 
          class="cancel-btn" 
          @click="handleClose"
          :disabled="isLoading"
        >
          取消
        </button>
        <button 
          class="confirm-btn" 
          @click="handleConfirm"
          :disabled="isLoading || !isValidCode"
        >
          {{ isLoading ? '验证中...' : '确认添加' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'

export default {
  name: 'AddDeviceDialog',
  props: {
    modelValue: {
      type: Boolean,
      required: true
    }
  },
  emits: ['update:modelValue', 'confirm'],
  setup(props, { emit }) {
    const authCode = ref('')
    const errorMessage = ref('')
    const successMessage = ref('')
    const isLoading = ref(false)

    // 验证码格式验证
    const isValidCode = computed(() => {
      return /^\d{6}$/.test(authCode.value)
    })

    // 处理输入，只允许数字
    const handleInput = (event) => {
      const value = event.target.value
      // 移除非数字字符
      authCode.value = value.replace(/\D/g, '')
    }

    // 监听输入变化，清除错误和成功消息
    watch(authCode, () => {
      errorMessage.value = ''
      successMessage.value = ''
    })

    // 监听对话框关闭，重置状态
    watch(() => props.modelValue, (newVal) => {
      if (!newVal) {
        resetState()
      }
    })

    const resetState = () => {
      authCode.value = ''
      errorMessage.value = ''
      successMessage.value = ''
      isLoading.value = false
    }

    const handleClose = () => {
      if (!isLoading.value) {
        emit('update:modelValue', false)
      }
    }

    const handleOverlayClick = () => {
      if (!isLoading.value) {
        emit('update:modelValue', false)
      }
    }

    const handleConfirm = async () => {
      // 验证输入
      if (!authCode.value.trim()) {
        errorMessage.value = '请输入设备认证码'
        return
      }

      if (!isValidCode.value) {
        errorMessage.value = '请输入6位数字认证码'
        return
      }

      isLoading.value = true
      errorMessage.value = ''
      successMessage.value = ''

      try {
        // 触发确认事件，将认证码传递给父组件
        const response = await emit('confirm', authCode.value.trim())
        
        // 只有在成功时才显示成功消息并关闭对话框
        if (response && response.status === 'success') {
          successMessage.value = '设备绑定成功！'
          
          // 1.5秒后关闭对话框
          setTimeout(() => {
            emit('update:modelValue', false)
            resetState()
          }, 1500)
        } else {
          throw new Error(response?.message || '添加设备失败')
        }
      } catch (error) {
        console.error('设备绑定失败:', error)
        errorMessage.value = error.message || '添加设备失败，请重试'
      } finally {
        isLoading.value = false
      }
    }

    return {
      authCode,
      errorMessage,
      successMessage,
      isLoading,
      isValidCode,
      handleInput,
      handleOverlayClick,
      handleConfirm,
      handleClose
    }
  }
}
</script>

<style scoped>
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

.close-btn:hover {
  color: #333;
}

.dialog-body {
  padding: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.auth-code-input {
  text-align: center;
  letter-spacing: 2px;
  font-family: Arial, sans-serif;
}

.auth-code-input::placeholder {
  text-align: left;
  letter-spacing: normal;
  font-family: Arial, sans-serif;
}

.form-group input:focus {
  outline: none;
  border-color: #313a7e;
}

.form-group input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.error-message, .success-message {
  font-size: 0.875rem;
  margin-top: 0.5rem;
  padding: 0.5rem;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.error-message {
  color: #dc3545;
  background-color: #fff5f5;
}

.success-message {
  color: #28a745;
  background-color: #f4faf6;
}

.error-icon, .success-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  font-size: 12px;
  font-weight: bold;
}

.error-icon {
  background-color: #dc3545;
  color: white;
}

.success-icon {
  background-color: #28a745;
  color: white;
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
  min-width: 80px;
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
  background-color: #313a7e;
  color: white;
  border: none;
}

.confirm-btn:hover:not(:disabled) {
  background-color: #252d63;
}

.cancel-btn:disabled,
.confirm-btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}
</style> 