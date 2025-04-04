<template>
  <div class="schedule">
    <div class="page-header">
      <h1>日程规划</h1>
      <p class="subtitle">科学安排时间，合理规划日程</p>
    </div>
    <div class="content-area">
      <div class="calendar-section">
        <div class="calendar-header">
          <button class="calendar-nav"><span>◀</span></button>
          <h2>2024年3月</h2>
          <button class="calendar-nav"><span>▶</span></button>
        </div>
        <div class="calendar-grid">
          <div class="calendar-weekdays">
            <span>日</span>
            <span>一</span>
            <span>二</span>
            <span>三</span>
            <span>四</span>
            <span>五</span>
            <span>六</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.schedule {
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

.calendar-section {
  width: 100%;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.calendar-header h2 {
  color: #333;
  font-size: 1.5rem;
}

.calendar-nav {
  background: none;
  border: none;
  color: #666;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.3s;
}

.calendar-nav:hover {
  background-color: #f5f5f5;
  color: #232b7e;
}

.calendar-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1rem;
  text-align: center;
  margin-bottom: 1rem;
}

.calendar-weekdays span {
  color: #666;
  font-weight: bold;
}

@media (max-width: 768px) {
  .schedule {
    padding: 1rem;
  }

  .content-area {
    padding: 1rem;
  }

  .calendar-weekdays {
    gap: 0.5rem;
  }
}
</style> 