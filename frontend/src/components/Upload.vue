<template>
  <div v-if="props.visible">

          <el-upload drag multiple
              :before-upload="handleBeforeUpload" class="mx-4" :http-request="fileUpload">
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
import { ossInstance } from '@/api/api'
import { ref } from 'vue'
import axios from 'axios'


const props = defineProps(['visible'])
const uploadData = ref({})
const uploadUrl = ref('')
const handleBeforeUpload = async (file) => {
  uploadData.value = new FormData();

  // 获取oss 签名
  const res = await ossInstance.get("/")
  const data = res.data

  uploadData.value.append("OSSAccessKeyId",data.accessid)
  uploadData.value.append("policy",data.policy)
  uploadData.value.append("signature",data.signature)
  uploadData.value.append("dir",data.dir)
  uploadData.value.append("key", data.dir + file.name)
  uploadData.value.append("host",data.host)
  uploadUrl.value = "http://" + data.host 
}

const fileUpload = async (option) => {
  let {file } = option
  uploadData.value.append("file",file)
  
  let res = await axios.post(uploadUrl.value, uploadData.value)
  if (res){
    delete uploadData.value
  }
  alert("上传成功")
}

</script>