
<template>


<div class="container">

    <Upload :visible="visible"/>
    <div class="search-box">
        <div>
            <label for="Search">Search:</label>
        <input type="text" id="Search" placeholder="Search..."/>
        </div>
        <el-button plain id="create" class="create" @click="visible=!visible" >创建</el-button>
    </div>

    <div class="list-box">
        <Capture v-for="capture in captures" :key="capture.id" :capture="capture" :username="data.username" />
    </div>

</div>
</template>

<script lang="ts" setup>
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessageBox, affixProps } from 'element-plus'
import Capture from '@/components/Capture.vue';
// import captures from '@/data/captures.json';
import {RouterView,useRouter} from 'vue-router';
import {ref,onMounted} from 'vue';
import Upload from '@/components/Upload.vue';
import {v4 as uuidv4} from 'uuid';
const uuid = uuidv4();
import {instance as api} from '@/api/api';

interface capture {
    id: number;
    info: {
        title: string;
        image_url: string;
        date: string;
        result_url: string;
        uuid: string;
    };
    status: {
        latest_run_current_stage: string;
        latest_run_status: string;
    };

}
interface data{
    captures: capture[];
    username: string;
    email: string;
    id: number;
    is_activate:true;

}


const visible = ref(false);
const router = useRouter();
const captures = ref<capture[]>([])
const data = ref<data>({
    captures: [],
    username: "",
    email: "",
    id: 0,
    is_activate: true

})


const loadCaptures = async() =>{
    const response =  await api.get("/captures/my/show",{
        headers:{
            Authorization: `Bearer ${localStorage.getItem("token")}`
        }
    })

    return response.data;
}
data.value = await loadCaptures();
captures.value = data.value.captures;

onMounted(async () => {
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

    } catch (error) {
        router.push('/login');
    }
})

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
        justify-content: flex-start;
        margin-top: 2%;
        margin-left: 10%;
    }
</style>
