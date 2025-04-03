<template>
  <div v-if="modelValue" class="dialog-overlay" @click="handleOverlayClick">
    <div class="dialog-content" @click.stop>
      <div class="dialog-header">
        <h3>添加设备</h3>
        <button class="close-btn" @click="$emit('update:modelValue', false)">×</button>
      </div>
      <div class="dialog-body">
        <div class="form-group">
          <label>设备认证码</label>
          <input 
            type="text" 
            v-model="authCode"
            placeholder="请输入设备认证码"
            :disabled="isLoading"
          />
          <div class="error-message" v-if="errorMessage">{{ errorMessage }}</div>
        </div>
      </div>
      <div class="dialog-footer">
        <button 
          class="cancel-btn" 
          @click="$emit('update:modelValue', false)"
          :disabled="isLoading"
        >
          取消
        </button>
        <button 
          class="confirm-btn" 
          @click="handleConfirm"
          :disabled="isLoading"
        >
          {{ isLoading ? '添加中...' : '确认添加' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

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
    const isLoading = ref(false)

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

      isLoading.value = true
      errorMessage.value = ''

      try {
        // 触发确认事件，将认证码传递给父组件
        await emit('confirm', authCode.value.trim())
        // 成功后关闭对话框
        emit('update:modelValue', false)
        // 清空输入
        authCode.value = ''
      } catch (error) {
        errorMessage.value = error.message || '添加设备失败，请重试'
      } finally {
        isLoading.value = false
      }
    }

    return {
      authCode,
      errorMessage,
      isLoading,
      handleOverlayClick,
      handleConfirm
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

.form-group input:focus {
  outline: none;
  border-color: #313a7e;
}

.form-group input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.error-message {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.5rem;
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
  background-color: #313a7e;
  color: white;
  border: none;
}

.confirm-btn:hover {
  background-color: #252d63;
}

.cancel-btn:disabled,
.confirm-btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}
</style> 