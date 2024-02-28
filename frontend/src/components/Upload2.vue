
<template>
    <el-upload
      ref="upload"
      action="https://f-test-bucket.oss-cn-hangzhou.aliyuncs.com" 
      :limit="1"
      :before-upload="handleBeforeUpload"
      :on-change="handleAddFile"
      :on-exceed="handleExceed"
      :auto-upload="false"
      :data="_selfOssSign"
    >
      <template #trigger>
        <el-button type="primary">select file</el-button>
      </template>
      <el-button class="ml-3" type="success" @click="submitUpload()">
        upload to server
      </el-button>
      <template #tip>
        <div class="el-upload__tip text-red">
          limit 1 file, new file will cover the old file
        </div>
      </template>
    </el-upload>
    <video controls width="320" height="240" :src="fileURL"></video>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { genFileId } from 'element-plus'
  import { defineEmits } from 'vue';
  import { DefineProps } from 'vue';
  import {ossInstance} from '@/api/api'
  
  const upload = ref(null)
  const fileURL = ref(null)
 
  let _selfOssSign =ref({
              'key': '',
              'OSSAccessKeyId': '',
              'policy': '',
             'signature': '',
              'host': '',
              'dir': '',
            }) 
  const emit = defineEmits(['notShowModal'])

  const handleClose = ()=> {
    emit('notShowModal')
  }

  const handleAddFile = (files) => {
    const file = files.raw
    fileURL.value = URL.createObjectURL(file)
    // 直接在这里写好FormData，按下按钮就上传，不通过 el-upload的 submit方法和 :data写参数了
  }
  
  const handleExceed = (files) => {
    upload.value.clearFiles()
    const file = files[0]
    file.uid = genFileId()
    upload.value.handleStart(file)
  }
  
  const handleBeforeUpload = (files) => {
// 先获取OSS 签名

    return new Promise((resolve, reject)=>{
      ossInstance.get("/").then(response=>{

            const data = response.data
            _selfOssSign.value.key = data.dir + files.name
            _selfOssSign.value.OSSAccessKeyId = data.accessid
            _selfOssSign.value.policy = data.policy
            _selfOssSign.value.signature = data.signature
            _selfOssSign.value.host = data.host
            _selfOssSign.value.dir = data.dir
            
            console.log(files)

            resolve(true)
      }).catch(error=>{
        console.log(error)
        alert("上传出错,看console")
        reject(false)
      });
    });
  };
  const submitUpload = () => {
    console.log(_selfOssSign.value)
    upload.value.submit()
  }
</script>
  