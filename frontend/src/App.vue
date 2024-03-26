
<template>
  <NavBar></NavBar>
    <!-- 异步加载组件 -->
    <Suspense>  
        <RouterView></RouterView>
    </Suspense>

</template>

<script lang="ts" setup>
  import { ref } from 'vue'
  import { RouterLink, RouterView } from 'vue-router'
  import NavBar from '@/components/NavBar.vue'

</script>
<style scoped>


</style>
  