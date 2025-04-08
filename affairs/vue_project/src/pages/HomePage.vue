<template>
  <div class="home">
    <div class="welcome-container">
      <h1 class="welcome-text">欢迎使用端侧AI管理系统</h1>
      <div class="welcome-subtitle">AI智能体</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage'
}
</script>

<style scoped>
.home {
  height: calc(100vh - 64px); /* 减去导航栏的高度 */
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f5f7ff 0%, #ffffff 100%);
  overflow: hidden;
  position: fixed;
  top: 64px; /* 导航栏高度 */
  left: 0;
  right: 0;
  bottom: 0;
}

.welcome-container {
  text-align: center;
  animation: fadeIn 1.5s ease-out;
  padding: 0 1rem;
  max-width: 100%;
}

.welcome-text {
  color: #313a7e;
  font-size: min(2.5rem, 8vw);
  margin-bottom: 1rem;
  opacity: 0;
  animation: slideUp 0.8s ease-out forwards;
  white-space: nowrap;
}

.welcome-subtitle {
  color: #666;
  font-size: min(1.2rem, 4vw);
  opacity: 0;
  animation: slideUp 0.8s ease-out 0.3s forwards;
  white-space: nowrap;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
