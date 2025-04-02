<template>
  <div class="app">
    <AppNav v-if="showNav" />
    <main :class="['main-content', { 'with-padding': showNav }]">
      <router-view></router-view>
    </main>
    <AppFooter v-if="showNav" />
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppNav from './components/AppNav.vue'
import AppFooter from './components/AppFooter.vue'

export default {
  name: 'App',
  components: {
    AppNav,
    AppFooter
  },
  setup() {
    const route = useRoute()
    const showNav = computed(() => {
      return !['Login', 'Register'].includes(route.name)
    })

    return {
      showNav
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app {
  min-height: 100vh;
  font-family: Arial, sans-serif;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
}

.main-content.with-padding {
  padding-bottom: 60px; /* 只有在显示导航栏和页脚时才添加底部内边距 */
}
</style>
