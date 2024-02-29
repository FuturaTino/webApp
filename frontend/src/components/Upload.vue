<template>
  <div class="container"  v-if="props.visible">
    <div>
      <label for="title">标题:</label>
      <el-input id="title" v-model="title" placeholder="请输入标题"></el-input>
    </div>

    <div>
      <el-radio-group v-model="visibility">
        <el-radio label="public">公开</el-radio>
        <el-radio label="private">仅自己查看</el-radio>
      </el-radio-group>
    </div>

    <el-upload drag multiple
        :before-upload="handleBeforeUpload" class="mx-4" :http-request="fileUpload" v-if="title">
        <el-icon class="el-icon--upload" style="height: 150px">
            <upload-filled />
        </el-icon>
        <div class="el-upload__text">
            将文件拖动到这里或者<em>点击上传</em>
        </div>
        <template #tip>
            <div class="el-upload__tip">文件不能超过100MB</div>
        </template>
    </el-upload>
  </div>
</template>

<script setup>
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessageBox } from 'element-plus'
import {defineProps} from 'vue'
import {defineEmits} from 'vue'
import { instance as api,ossInstance } from '@/api/api'
import { ref } from 'vue'
import axios from 'axios'
import {v4 as uuidv4} from 'uuid'

// 上传调度服务器的form基本信息
const title = ref('')
const visibility = ref('public')
const uuid = ref('')

// 上传Oss服务器的基本信息 
const props = defineProps(['visible'])
const uploadData = ref({})
const uploadUrl = ref('')
const handleBeforeUpload = async (file) => {
  uploadData.value = new FormData();
  uuid.value = uuidv4()
  // 获取oss 签名
  const res = await ossInstance.get("/")
  const data = res.data

  uploadData.value.append("OSSAccessKeyId",data.accessid)
  uploadData.value.append("policy",data.policy)
  uploadData.value.append("signature",data.signature)
  uploadData.value.append("dir",data.dir)
  uploadData.value.append("key", data.dir + uuid.value + ".mp4")
  uploadData.value.append("host",data.host)
  uploadUrl.value = "http://" + data.host 
}

const fileUpload = async (option) => {
  try{
    let {file } = option
    uploadData.value.append("file",file)
  
    let res = await axios.post(uploadUrl.value, uploadData.value)
    if (res){
      delete uploadData.value
    }
    alert("上传成功")
    handleAfterUpload()
  } catch(error){
    console.log(error)
    alert("上传失败",error)
  }

}

const handleAfterUpload = async ()=>{
  const formData ={
    "title": title.value,
    "uuid": uuid.value,
  }
  const token = localStorage.getItem("token")
  const body = new URLSearchParams(formData)
  const response_create = await api.post("captures/my/create",body,{
      headers: {"Authorization": `Bearer ${token}`,
     'Content-Type': 'application/x-www-form-urlencoded'
    }
  })
}
  
</script>

<style scoped>
.container{
  display: flex;
  flex-direction: column;
  width: 80%;

  border-radius: 2%;
  box-shadow: 1px 1px 10px rgba(0,0,0,0.1);
  padding-block: 2%;
  padding-inline: 1%;
  margin-bottom: 3%;
}
</style>