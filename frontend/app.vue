<template>
  <div> 
    <div v-for="user in users">
      <h1>{{ user.email }}</h1>
    </div>
  </div>
</template>


<script setup>
  const { data: {value: { users } } } = await useBaseFetch('/users')
</script>