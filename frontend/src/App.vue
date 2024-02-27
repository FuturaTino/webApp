<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Capture  from './components/Capture.vue';

</script>

<template>
    <RouterLink to="/register">Register</RouterLink>
    <RouterLink to="/login"> Login</RouterLink>
    <RouterLink to="/home"> Home</RouterLink>
    <RouterView></RouterView>
</template>

<style scoped>

</style>
