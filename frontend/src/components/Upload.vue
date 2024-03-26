<template>
  <div class="container"  v-if="props.visible">
    <div>
      <label for="title">标题:</label>
      <el-input id="title" v-model="title" placeholder="请输入标题"></el-input>
    </div>
    <div>
      <label for="iterations">迭代次数:</label>
      <el-input id="iterations" v-model="iterations" placeholder="输入迭代次数" ></el-input>
    </div>

    <div>
      <label for="feature_lr">特征的学习率:</label>
      <el-input id="feature_lr" v-model="feature_lr" placeholder="输入特征的学习率"></el-input>
    </div>


    <div>
      <label>不透明度阈值:</label>
      <el-radio-group v-model="opacity_threshold">
        <el-radio :label="0.004">0.004</el-radio>
        <el-radio :label="0.005">0.005</el-radio>
        <el-radio :label="0.006">0.006</el-radio>
      </el-radio-group>
    </div>

    <div>
      <label>尺寸阈值:</label>
      <el-radio-group v-model="size_threshold">
        <el-radio :label="18">18</el-radio>
        <el-radio :label="20">20</el-radio>
        <el-radio :label="22">22</el-radio>
      </el-radio-group>
    </div>

    <div>
      <label>不透明度重置间隔:</label>
      <el-radio-group v-model="opacity_reset_interval">
        <el-radio :label="2800">2800</el-radio>
        <el-radio :label="3000">3000</el-radio>
        <el-radio :label="3200">3200</el-radio>
      </el-radio-group>
    </div>

    <div>
      <label>稠密化操作的间隔:</label>
      <el-radio-group v-model="densification_interval">
        <el-radio :label="90">90</el-radio>
        <el-radio :label="100">100</el-radio>
        <el-radio :label="110">110</el-radio>
      </el-radio-group>
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
            <div class="el-upload__tip">文件不能超过4096MB</div>
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
const iterations = ref(30000)
const feature_lr = ref(0.00016)
const opacity_threshold = ref(0.004)
const size_threshold = ref(18)
const opacity_reset_interval = ref(2800)
const densification_interval = ref(90)
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
  console.log("formData",formData)

  const token = localStorage.getItem("token")

  // Post调度服务器，创建Capture
  const body = new URLSearchParams(formData)
  const response_create = await api.post("captures/my/create",body,{
      headers: {"Authorization": `Bearer ${token}`,
     'Content-Type': 'application/x-www-form-urlencoded'
    }
  })
  console.log("response_create",response_create)
 
  // Post调度服务器，处理Capture
  if (response_create.status === 200){
    const response_process = await api.post("captures/process",null,{
      params:{
        uuid: uuid.value,
      },
      headers:{"Authorization": `Bearer ${token}`},
    })
  }
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
label {
  margin-right: 10px;
}
</style>