<template>
  <div class="home">
    <div class="welcome-section">
      <h1 class="welcome-title animate-slide-down">欢迎来到 LFNL 个人系统</h1>
      <p class="welcome-subtitle animate-fade-in">您的智能工作助手</p>
      <div class="feature-cards">
        <div class="card animate-slide-up">
          <div class="card-icon">📊</div>
          <h3>数据分析</h3>
          <p>智能数据处理，轻松掌握信息</p>
        </div>
        <div class="card animate-slide-up" style="animation-delay: 0.2s">
          <div class="card-icon">⏱️</div>
          <h3>效率提升</h3>
          <p>优化时间管理，提高工作效率</p>
        </div>
        <div class="card animate-slide-up" style="animation-delay: 0.4s">
          <div class="card-icon">🎯</div>
          <h3>目标达成</h3>
          <p>科学规划目标，逐步实现理想</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  min-height: calc(100vh - 64px);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  padding: 2rem;
}

.welcome-section {
  text-align: center;
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-title {
  font-size: 2.5rem;
  color: #232b7e;
  margin-bottom: 1rem;
  font-weight: bold;
}

.welcome-subtitle {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 3rem;
}

.feature-cards {
  display: flex;
  gap: 2rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 3rem;
}

.card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 280px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.card:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.card-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.card h3 {
  color: #232b7e;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.card p {
  color: #666;
  font-size: 0.9rem;
}

/* 动画效果 */
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-down {
  animation: slideDown 0.8s ease forwards;
}

.animate-fade-in {
  animation: fadeIn 1s ease forwards;
  animation-delay: 0.3s;
  opacity: 0;
}

.animate-slide-up {
  animation: slideUp 0.8s ease forwards;
  animation-delay: 0.6s;
  opacity: 0;
}

@media (max-width: 768px) {
  .welcome-title {
    font-size: 2rem;
  }

  .welcome-subtitle {
    font-size: 1rem;
    margin-bottom: 2rem;
  }

  .feature-cards {
    gap: 1rem;
  }

  .card {
    width: 100%;
    max-width: 300px;
    padding: 1.5rem;
  }
}
</style> 