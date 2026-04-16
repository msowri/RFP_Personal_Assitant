<template>

  <div class="home">

    <!-- <div data-msg> {{ message }}</div> -->
    <!-- <Header /> -->

    <!-- <main class="content">
      <h1>FRP Personal Assistant</h1>

      <p>
        This is the home page.
      </p>

      <button @click="clickHandler">
        Click
      </button>

    </main> -->

    <!-- <Footer /> -->

  </div>

</template>

<script setup lang="ts">
import { ref } from 'vue'
const message = ref('Hello, Vue 3 with TypeScript!')

//  import Header from './Header.vue'
//  import Footer from './Footer.vue'

function clickHandler(){
  alert("Vue + TypeScript Working!")
}
</script>

