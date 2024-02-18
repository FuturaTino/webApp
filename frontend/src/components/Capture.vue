<script setup>
const capture = {
  'title': 'Hello Vue 3',
  'owner': 'John Doe',
  'date': '2022-01-01',
  "image": "http://localhost:5173/img.png",
}

</script>

<template>
  <div class="capture">
    <div class="img">
      <img v-bind:src="capture.image" alt="img">
      <p>{{ capture.date }}</p>
    </div>

    <h2>{{ capture.title }}</h2>
    <p>@{{ capture.owner }}</p>

  </div>
</template>

<style scoped>
.capture {
  width: 20%; /* capture 占屏幕的 25% */
  aspect-ratio: 1 / 1; /* 使 capture 为正方形 */
  border: 1px solid;
  border-radius: 5%; /* 设置 border 的圆角为 25% */
  text-align: center;
  font-size: 12px; /* 设置字体大小为 12px */
  box-sizing: border-box; /* 包括 padding 和 border 在内的宽度和高度 */
}

.capture img {
  max-width: 80%; /* 图片最大宽度为 100% */
  height: auto; /* 高度自动 */;
}
</style>
