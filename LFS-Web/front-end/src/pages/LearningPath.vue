<template>
  <div class="learning-path">
    <div class="page-header">
      <h1>学习路径</h1>
      <p class="subtitle">定制专属学习计划，追踪学习进度</p>
    </div>
    <div class="content-area">
      <div class="path-container">
        <div class="path-item">
          <div class="path-status completed">✓</div>
          <div class="path-content">
            <h3>基础知识</h3>
            <p>掌握核心概念和基本理论</p>
            <div class="progress-bar">
              <div class="progress" style="width: 100%"></div>
            </div>
          </div>
        </div>
        <div class="path-connector"></div>
        <div class="path-item">
          <div class="path-status in-progress">⋯</div>
          <div class="path-content">
            <h3>进阶学习</h3>
            <p>深入专业领域，提升实践能力</p>
            <div class="progress-bar">
              <div class="progress" style="width: 60%"></div>
            </div>
          </div>
        </div>
        <div class="path-connector"></div>
        <div class="path-item">
          <div class="path-status">○</div>
          <div class="path-content">
            <h3>高级技能</h3>
            <p>专业技能提升，项目实战演练</p>
            <div class="progress-bar">
              <div class="progress" style="width: 0%"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.learning-path {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
  text-align: center;
}

.page-header h1 {
  color: #232b7e;
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666;
  font-size: 1.1rem;
}

.content-area {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

.path-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
}

.path-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  transition: transform 0.3s;
}

.path-item:hover {
  transform: translateX(10px);
}

.path-status {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: #666;
}

.path-status.completed {
  background-color: #28a745;
  color: white;
}

.path-status.in-progress {
  background-color: #007bff;
  color: white;
}

.path-content {
  flex: 1;
}

.path-content h3 {
  color: #333;
  margin-bottom: 0.5rem;
}

.path-content p {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.progress-bar {
  height: 6px;
  background-color: #e9ecef;
  border-radius: 3px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: #232b7e;
  transition: width 0.3s ease;
}

.path-connector {
  width: 2px;
  height: 20px;
  background-color: #e9ecef;
  margin-left: 47px;
}

@media (max-width: 768px) {
  .learning-path {
    padding: 1rem;
  }

  .content-area {
    padding: 1rem;
  }

  .path-item {
    padding: 0.8rem;
  }

  .path-item:hover {
    transform: none;
  }
}
</style> 