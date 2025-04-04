<template>
  <nav class="navbar">
    <router-link to="/" class="navbar-brand" style="cursor: pointer" :class="{ 'no-active': true }">
      LFNL TECH
    </router-link>
    <button class="menu-toggle" @click="toggleMenu">
      <span class="bar"></span>
      <span class="bar"></span>
      <span class="bar"></span>
    </button>
    <div class="navbar-menu" :class="{ 'is-active': isMenuOpen }">
      <router-link to="/time" class="nav-item">时间管理</router-link>
      <router-link to="/schedule" class="nav-item">日程规划</router-link>
      <router-link to="/learning" class="nav-item">学习路径</router-link>
      <router-link to="/about" class="nav-item">关于我们</router-link>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'

const isMenuOpen = ref(false)
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}
</script>

<style scoped>
.navbar {
  width: 100%;
  height: 64px;
  background-color: #232b7e;
  display: flex;
  align-items: center;
  padding: 0 48px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
}

.navbar-brand {
  color: white;
  font-size: 24px;
  font-weight: bold;
  letter-spacing: 1px;
  transition: opacity 0.3s;
  text-decoration: none;
}

.navbar-brand:hover {
  opacity: 0.8;
}

/* 禁止标题链接高亮 */
.navbar-brand.router-link-active {
  background-color: transparent;
  font-weight: bold;
}

/* 使用no-active类来覆盖active样式 */
.no-active.router-link-active {
  background-color: transparent !important;
}

.navbar-menu {
  display: flex;
  margin-left: 60px;
  gap: 32px;
}

.nav-item {
  color: white;
  text-decoration: none;
  font-size: 16px;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background-color 0.3s;
  cursor: pointer;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.router-link-active {
  background-color: rgba(255, 255, 255, 0.15);
  font-weight: bold;
}

.menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 30px;
  height: 21px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  margin-left: auto;
}

.bar {
  width: 100%;
  height: 3px;
  background-color: white;
  border-radius: 3px;
  transition: all 0.3s;
}

@media (max-width: 768px) {
  .navbar {
    padding: 0 20px;
  }

  .menu-toggle {
    display: flex;
  }

  .navbar-menu {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background-color: #232b7e;
    margin-left: 0;
    flex-direction: column;
    padding: 1rem;
    gap: 16px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    z-index: 100;
  }

  .navbar-menu.is-active {
    display: flex;
  }

  .nav-item {
    width: 100%;
    text-align: center;
  }
}

/* 平板电脑布局 */
@media (min-width: 769px) and (max-width: 1024px) {
  .navbar {
    padding: 0 30px;
  }

  .navbar-menu {
    margin-left: 30px;
    gap: 20px;
  }

  .nav-item {
    padding: 6px 12px;
    font-size: 15px;
  }
}
</style>
