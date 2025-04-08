<template>
  <div class="about">
    <div class="page-header">
      <h1 class="animate-slide-down">关于我们</h1>
      <p class="subtitle animate-fade-in">了解LFNL TECH的理念与使命</p>
    </div>
    
    <div class="content-area animate-slide-up">
      <div class="about-section">
        <h2>我们的愿景</h2>
        <p>LFNL TECH致力于通过智能化的个人管理系统，帮助用户更高效地规划时间、设定目标并实现个人成长。我们相信，每个人都可以通过科学的方法和适合自己的工具，充分发挥潜能，实现自我价值。</p>
        
        <div class="about-cards">
          <div class="about-card">
            <h3>我们的使命</h3>
            <p>提供简单易用、功能强大的个人管理工具，帮助用户建立高效工作习惯，平衡工作与生活。</p>
          </div>
          
          <div class="about-card">
            <h3>我们的价值观</h3>
            <p>用户至上、注重隐私、持续创新、简约设计，是我们产品开发和服务的核心理念。</p>
          </div>
        </div>
        
        <div class="team-section">
          <h2>我们的团队</h2>
          <p>LFNL TECH由一群热爱科技、关注用户体验的专业人士组成。我们拥有丰富的行业经验和创新思维，致力于打造最优质的个人管理系统。</p>
        </div>
        
        <div class="contact-section">
          <h2>联系我们</h2>
          <p>如果您有任何问题、建议或合作意向，欢迎随时与我们联系。</p>
          <div class="contact-info">
            <div>
              <strong>邮箱：</strong> lfnltech@163.com
            </div>
            <div>
              <strong>地址：</strong> 中国 · 南京
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.about {
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
  margin-bottom: 2rem;
}

.content-area {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

.about-section h2 {
  color: #232b7e;
  font-size: 1.5rem;
  margin: 1.5rem 0 1rem;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 0.5rem;
}

.about-section p {
  color: #333;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.about-cards {
  display: flex;
  gap: 2rem;
  margin: 2rem 0;
  flex-wrap: wrap;
}

.about-card {
  flex: 1;
  min-width: 300px;
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.about-card:hover {
  transform: translateY(-5px);
}

.about-card h3 {
  color: #232b7e;
  margin-bottom: 1rem;
}

.contact-info {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-top: 1rem;
}

.contact-info div {
  margin-bottom: 0.5rem;
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
  animation-delay: 0.5s;
  opacity: 0;
}

@media (max-width: 768px) {
  .about {
    padding: 1rem;
  }

  .content-area {
    padding: 1.5rem;
  }

  .about-cards {
    flex-direction: column;
    gap: 1rem;
  }

  .page-header h1 {
    font-size: 1.8rem;
  }
}
</style> 