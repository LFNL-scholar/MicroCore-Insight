<script setup>
import Navbar from './components/Navbar.vue'
</script>

<template>
  <div class="app">
    <Navbar />
    <router-view />
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background-color: #f5f5f5;
}

.app {
  min-height: 100vh;
  font-family: Arial, sans-serif;
}

.content {
  padding: 40px;
  text-align: center;
}

h1 {
  color: #333;
  margin-top: 20px;
}
</style>
