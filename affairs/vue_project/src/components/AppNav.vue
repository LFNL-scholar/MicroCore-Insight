<template>
  <nav class="navbar">
    <div class="nav-left">
      <div class="navbar-brand" @click="goToHome"><b>端侧AI</b></div>
      <div class="nav-links">
        <div 
          class="nav-link" 
          :class="{ active: isConsolePage }"
          @click="goToConsole"
        >
          控制台
        </div>
      </div>
    </div>
    <div class="user-menu" @click="toggleDropdown" ref="userMenuRef">
      <img src="../assets/user.png" alt="用户" class="user-icon">
      <span class="username">{{ username }}</span>
      <div class="dropdown-menu" v-show="isDropdownOpen">
        <div class="dropdown-item" @click="goToSettings">
          <img src="../assets/setting.png" alt="设置" class="menu-icon">
          账号设置
        </div>
        <div class="dropdown-item" @click="logout">
          <img src="../assets/quit.png" alt="退出" class="menu-icon">
          退出登录
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getUserInfo } from '../api/user'

export default {
  name: 'AppNav',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const username = ref('管理员')  // 默认显示"管理员"
    const isDropdownOpen = ref(false)
    const userMenuRef = ref(null)

    const isConsolePage = computed(() => {
      return route.name === 'Console'
    })

    // 加载用户信息
    const loadUserInfo = async () => {
      try {
        const userId = localStorage.getItem('userId')
        if (!userId) {
          console.log('未找到用户ID，使用默认昵称')
          return
        }

        const response = await getUserInfo(userId)
        if (response && response.status === 'success') {
          username.value = response.nickname || '管理员'
          console.log('已更新用户昵称:', username.value)
        }
      } catch (error) {
        console.error('加载用户昵称失败:', error)
        // 失败时保持默认昵称
      }
    }

    const toggleDropdown = () => {
      isDropdownOpen.value = !isDropdownOpen.value
    }

    const goToHome = () => {
      router.push('/home')
    }

    const goToConsole = () => {
      router.push('/console')
    }

    const goToSettings = () => {
      isDropdownOpen.value = false
      router.push('/settings')
    }

    const logout = () => {
      isDropdownOpen.value = false
      // 清除用户登录状态
      localStorage.clear()
      router.push('/login')
    }

    const handleClickOutside = (event) => {
      if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
        isDropdownOpen.value = false
      }
    }

    onMounted(() => {
      document.addEventListener('click', handleClickOutside)
      // 组件挂载时加载用户信息
      loadUserInfo()
    })

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
    })

    return {
      username,
      isDropdownOpen,
      userMenuRef,
      isConsolePage,
      toggleDropdown,
      goToHome,
      goToConsole,
      goToSettings,
      logout
    }
  }
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
  height: 64px;
  background-color: #313a7e; 
  color: white;
  position: relative;
  z-index: 1000;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.navbar-brand {
  font-size: 1.25rem;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.2s;
}

.navbar-brand:hover {
  opacity: 0.8;
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-link {
  padding: 0.5rem 1rem;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-link.active {
  background-color: rgba(255, 255, 255, 0.2);
}

.user-menu {
  position: relative;
  cursor: pointer;
  padding: 8px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.user-icon {
  width: 15px;
  height: 15px;
  object-fit: contain;
}

.username {
  font-size: 1rem;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  min-width: 120px;
  margin-top: 4px;
  z-index: 1000;
}

.dropdown-item {
  color: #333;
  padding: 8px 16px;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.dropdown-item:hover {
  background-color: #f5f5f5;
}

.menu-icon {
  width: 15px;
  height: 15px;
  object-fit: contain;
}
</style>
