<script setup>
import { ref } from 'vue'
import api from "@/api/api"
import {defineEmits} from 'vue'
const captureUrl= ref('');
const file = ref(null);
const title = ref('');

const emits = defineEmits(['notShowModal'])
const formdata = new FormData();

const handleFileChange = (e) => {
    captureUrl.value = URL.createObjectURL(e.target.files[0]); //这是什么? url
    file.value = e.target.files[0];
    console.log('captureUrl.value')
    console.log(captureUrl.value);
    console.log("file.value")
    console.log(file.value);
}

const createCapture = ()=> {
    const token = localStorage.getItem("token");
    formdata.append("file", file.value);
    formdata.append("title", title.value);
    api.post("/captures/my/create",formdata,{
        headers: {
            'Content-Type':'multipart/form-data',
            Authorization: `Bearer ${token}`
        }
    }).then(response=>{
            console.log(response);
            //上传进度
            alert("创建成功");
            emits('notShowModal'); //不用参数
    })
}
</script>

<template>
    <div class="container">

        <form @submit.prevent="createCapture">
            <h1>创建 Capture</h1>
            <video id="capture-video" v-if="captureUrl" :src="captureUrl" controls ></video>
            <div v-if="captureUrl">
                <label for="title">标题：</label>
                <input id ="title" type="text" v-model="title" placeholder="标题" required>
            </div>
            <input type="file" id="capture-file" @change="handleFileChange">


        </form>
        <button type="submit" @click="createCapture">提交</button>
    </div>
</template>

<style scoped>
    .container{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 500px;
        height: auto;
        margin-bottom: 50px;
    }
    .container button {
        margin-top: 20px;
        margin-left: 50px;
        margin-bottom:50px;
    }

    #capture-video {
        width: 320px;
        height: 225px;
    }
</style>


