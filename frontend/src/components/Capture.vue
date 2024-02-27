<script setup>
import captures from "@/data/captures.json" 
import { ref } from "vue"
import { defineProps } from "vue";

const props = defineProps(["capture"])
</script>

<template>
  <div class="capture">
      <img :src="capture.image_url" alt="">
      <div class="capture-text">
          <h2>{{ capture.title }}</h2>
        <p>@author: {{ capture.owner }}</p>
      </div>
  </div>
</template>

<style scoped>
    .capture {
    width: 310px;
    overflow: hidden;
    border-radius: 2%;
    box-shadow: 1px 1px 10px rgba(0,0,0,0.1);
    margin-bottom: 5%;
    margin-inline: 1%;
    cursor: pointer;
  }

  .capture img {
    width: 100%;
    overflow: hidden;
    height: 225px;
    margin: 0
  }

  .capture .capture-text {
    padding: 0 5px
  }

  .card .card-text h2 {
    font-weight: bold;
  }
</style>