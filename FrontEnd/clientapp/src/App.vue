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

<style>

.app-container{
  display:flex;
  flex-direction:column;
  min-height:98vh;
}

.content{
  flex:1;
  padding:20px;
}

</style>
