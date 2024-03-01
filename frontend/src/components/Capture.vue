<template>
  <div class="capture" @click="loadRenderView()">
      <div class="img-box" style="text-align:center;">
        <img  :src="capture.info.image_url" > 
        <p v-if="capture.status.latest_run_current_stage !== 'Finished'">{{ capture.status.latest_run_current_stage }}</p>
      </div>

      <div class="capture-text">
          <h2>标题：{{ capture.info.title }}</h2>
        <p>作者: {{ username }}</p>
        <p>创建：{{ capture.info.date }}</p>
      </div>
  </div>
</template>

<script setup>
import captures from "@/data/captures.json" 
import { ref } from "vue"
import { defineProps } from "vue";
import {useRouter,useRoute} from "vue-router";

const props = defineProps(["capture","username"])
const router = useRouter()
const route = useRoute()

const loadRenderView = ()=>{
  router.push({
    path:`/home/${props.capture.info.uuid}`,
    query:{
      username: props.username,
      result_url : props.capture.info.result_url
    }
  })  
}
</script>

<style scoped>
    .capture {
    width: 310px;
    overflow: hidden;
    border-radius: 2%;
    box-shadow: 1px 1px 10px rgba(0,0,0,0.1);
    margin-bottom: 5%;
    margin-inline: 1%;
    cursor: pointer;
    height: fit-content;
  }

  .img-box img {
    width: 310px;
    overflow: hidden;
    height: 225px;
    margin: 0;
    object-fit: cover;
    object-position: center;
  }
  .img-box {
    display: flex;
    flex-direction: column;
    position: relative;
      object-fit: cover;
  }
  .img-box p {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }

  .capture .capture-text {
    padding: 0 5px
  }

  .card .card-text h2 {
    font-weight: bold;
  }
</style>