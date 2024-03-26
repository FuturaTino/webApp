<script setup>

</script>

<template>
    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      :ellipsis="false"
      @select="handleSelect"
    >

        <div class="flex-grow" />
        <el-menu-item index="4"><RouterLink to="/index">主页</RouterLink></el-menu-item>
        <el-menu-item index="3"><RouterLink to="/home">我的作品</RouterLink></el-menu-item>
        <el-menu-item index="2"><RouterLink to="/register">注册</RouterLink></el-menu-item>
        <el-menu-item index="1"><RouterLink to="/login">登录</RouterLink></el-menu-item>

    </el-menu>

    <!-- 异步加载组件 -->
    <Suspense>  
        <RouterView></RouterView>
    </Suspense>

</template>




<script lang="ts" setup>
  import { ref } from 'vue'
  import { RouterLink, RouterView } from 'vue-router'
    import Capture  from './components/Capture.vue';
    import testing from './views/testing.vue';
  const activeIndex = ref('1')
  const handleSelect = (key:string, keyPath:string[]) => {
    console.log(key, keyPath)
  }
</script>
  
<style scoped>
  .flex-grow {
    flex-grow: 1;
  }
   
   .el-menu-demo {
    margin-bottom: 20px;
   }

</style>
  