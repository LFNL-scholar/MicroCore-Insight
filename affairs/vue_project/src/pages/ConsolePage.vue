<template>
  <div class="console-container">
    <h1>控制台</h1>
    <div class="console-content">
      <!-- 这里添加控制台的具体内容 -->
      <div class="welcome-message">
        欢迎使用小智AI控制台
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConsolePage',
  setup() {
    // 控制台页面的逻辑
  }
}
</script>

<style scoped>
.console-container {
  padding: 2rem;
}

h1 {
  color: #313a7e;
  margin-bottom: 2rem;
}

.console-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.welcome-message {
  font-size: 1.2rem;
  color: #666;
}
</style> 