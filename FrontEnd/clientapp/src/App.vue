<template>

  <div class="app-container">

    <Header />

    <main class="content">
      <router-view />
    </main>

    <Footer />

  </div>

</template>

<script setup lang="ts">
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
</script>

