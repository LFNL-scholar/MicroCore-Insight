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
        <label>角色介绍</label>
        <textarea 
          v-model="roleDescription" 
          placeholder="请输入角色介绍"
          class="input-field textarea"
          rows="6"
        ></textarea>
      </div>
      <div class="button-group">
        <button class="reset-btn" @click="handleReset">重置</button>
        <button class="save-btn" @click="handleSave">保存</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'RoleConfigPage',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const deviceId = route.params.deviceId

    const roleName = ref('')
    const roleDescription = ref('')

    const handleBack = () => {
      router.push('/console')
    }

    const handleSave = () => {
      // 这里添加保存逻辑
      console.log('保存角色配置', {
        deviceId,
        roleName: roleName.value,
        roleDescription: roleDescription.value
      })
    }

    const handleReset = () => {
      roleName.value = ''
      roleDescription.value = ''
    }

    return {
      roleName,
      roleDescription,
      handleSave,
      handleReset,
      handleBack
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
</style> 