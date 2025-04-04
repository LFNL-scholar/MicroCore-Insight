<template>
  <div class="time-management">
    <div class="page-header">
      <h1>时间管理</h1>
      <p class="subtitle">合理规划时间，提高工作效率</p>
    </div>
    <div class="content-area">
      <div class="time-block">
        <h2>今日待办</h2>
        <div class="task-list">
          <div class="task-item">
            <input type="checkbox" id="task1">
            <label for="task1">完成项目规划</label>
          </div>
          <div class="add-task">
            <button class="add-btn">+ 添加任务</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.time-management {
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

.time-block {
  margin-bottom: 2rem;
}

.time-block h2 {
  color: #333;
  font-size: 1.5rem;
  margin-bottom: 1rem;
  border-bottom: 2px solid #eee;
  padding-bottom: 0.5rem;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.task-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border-radius: 6px;
  transition: background-color 0.3s;
}

.task-item:hover {
  background-color: #f5f5f5;
}

.task-item label {
  cursor: pointer;
  color: #333;
}

.add-task {
  margin-top: 1rem;
}

.add-btn {
  background: none;
  border: 2px dashed #ccc;
  color: #666;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  width: 100%;
  transition: all 0.3s;
}

.add-btn:hover {
  border-color: #232b7e;
  color: #232b7e;
}

@media (max-width: 768px) {
  .time-management {
    padding: 1rem;
  }

  .content-area {
    padding: 1rem;
  }
}
</style> 