<template>
  <nav class="navbar">
    <div class="navbar-brand" @click="goToHome"><b>小智AI</b></div>
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
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'AppNav',
  setup() {
    const router = useRouter()
    const username = ref('小云') 
    const isDropdownOpen = ref(false)
    const userMenuRef = ref(null)

    const toggleDropdown = () => {
      isDropdownOpen.value = !isDropdownOpen.value
    }

    const goToHome = () => {
      router.push('/home')
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
      toggleDropdown,
      goToHome,
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
