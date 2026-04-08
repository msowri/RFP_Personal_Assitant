<template>
  <header class="header">
    <div class="container">
      <h2 class="logo">My Vue App</h2>

      <nav>
        <ul>
          <!-- <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/about">About</router-link></li> -->
        </ul>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
</script>

<style scoped>

.header{
  background:#2c3e50;
  color:white;
  padding:3px;
}

.container{
  display:flex;
  justify-content:space-between;
  align-items:center;
}

nav ul{
  display:flex;
  gap:20px;
  list-style:none;
}

nav a{
  color:white;
  text-decoration:none;
}

.logo{
  font-weight:bold;
}

</style>
