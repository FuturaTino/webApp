<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Capture  from './components/Capture.vue';
import testing from './views/testing.vue';
</script>

<template>
    <RouterLink to="/register">Register</RouterLink>
    <RouterLink to="/login"> Login</RouterLink>
    <RouterLink to="/home"> Home</RouterLink>
    <RouterLink to="/test"> Testing</RouterLink>
    
    <RouterView></RouterView>
</template>

<style scoped>

</style>
