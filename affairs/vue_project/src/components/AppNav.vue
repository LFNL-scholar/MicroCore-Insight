<template>
  <nav class="navbar">
    <div class="nav-left">
      <div class="navbar-brand" @click="goToHome"><b>小智AI</b></div>
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
      <span class="username">{{ username }}</span>
      <div class="dropdown-menu" v-show="isDropdownOpen">
        <div class="dropdown-item" @click="goToSettings">账号设置</div>
        <div class="dropdown-item" @click="logout">退出登录</div>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

export default {
  name: 'AppNav',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const username = ref('小云') 
    const isDropdownOpen = ref(false)
    const userMenuRef = ref(null)

    const isConsolePage = computed(() => {
      return route.name === 'Console'
    })

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
      // localStorage.removeItem('token') // 如果有token的话
      router.push('/login')
    }

    const handleClickOutside = (event) => {
      if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
        isDropdownOpen.value = false
      }
    }

    onMounted(() => {
      document.addEventListener('click', handleClickOutside)
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
}

.dropdown-item:hover {
  background-color: #f5f5f5;
}
</style>
