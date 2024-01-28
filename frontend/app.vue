<template>
  <div> 
    <div v-for="user in users">
      <h1>{{ user.email }}</h1>
    </div>
  </div>
</template>


<script setup>
  const { data: users } = await useBaseFetch('/users')
</script>