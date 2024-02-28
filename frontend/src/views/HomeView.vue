
<template>

<h1>HomeView</h1>
加载界面前要请求后端verify token
<div class="container">
    {{ uuid }}
    <Upload :visible="visible"/>
    <div class="search-box">
        <div>
            <label for="Search">Search:</label>
        <input type="text" id="Search" placeholder="Search..."/>
        </div>
        <el-button plain id="create" class="create" @click="visible=!visible" >创建</el-button>
    </div>
    <div class="list-box">
        <Capture v-for="capture in captures" :key="capture.id" :capture="capture"/>
    </div>

</div>
</template>

<script setup>
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessageBox, affixProps } from 'element-plus'
import Capture from '@/components/Capture.vue';
import captures from '@/data/captures.json';
import {RouterView,useRouter} from 'vue-router';
import {ref} from 'vue';
import Upload from '@/components/Upload.vue';
import {v4 as uuidv4} from 'uuid';
const uuid = uuidv4();
import {instance as api} from '@/api/api';



const visible = ref(false);
const router = useRouter();

const onWindowLoad = async () => {
    // verify the token.
    const token = localStorage.getItem("token");
    const paramsString = `token=${token}`
    const searchParams = new URLSearchParams(paramsString)
    try {
        const response = await api.get("/auth/token",{
            params:{
                token:token
            },

        })
        console.log(response);
    } catch (error) {
        console.log(error);
        router.push('/login');
    }

}

onWindowLoad();

window.onbeforeunload = ()=>{
    localStorage.removeItem("token");
}
</script>

<style scoped>
    .container {
        width: 100%;
        display: flex;
        flex-wrap: wrap;
        flex-direction: column;

        justify-content: flex-start;
        margin:auto;
    }
    .container .search-box {
        display: flex;
        justify-content:space-evenly;

    }

    .search-box label {
        font-weight: bold;
        margin-right: 10px;
    }

    .search-box input {
        border: none;
        background-color: rgba(128,128,128, 0.1);
        padding: 10px;
        border-radius: 5px;
    }
    .list-box {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        margin-top: 2%;
    }
</style>
