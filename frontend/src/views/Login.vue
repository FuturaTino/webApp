<template>
    <div class="login-page">
        <div class="login-header">
            
        </div>
        <div class="login-panel">
            <div class="logo">
                <el-image :src="logoImage" class="logo-img"></el-image>
            </div>
            <div class="login-text">
                {{ loginText }}
            </div>
            <div class="login-form">
                <el-form ref="loginFormRef" :model="loginFormData" size="large" :rules="rules">
                    <el-form-item label="" prop="username" >
                        <el-input prefix-icon="Avatar" v-model="loginFormData.username" placeholder="请输入用户名"></el-input>
                    </el-form-item>
                    <el-form-item  label="" prop="password">
                        <el-input prefix-icon="Lock" type="password" v-model="loginFormData.password" placeholder="请输入密码"></el-input>
                    </el-form-item>
                    
                    <el-row>

                    </el-row>
                    <div class="check-line">
                        <div>
                            <el-col :span="12">
                                <el-checkbox v-model="loginFormData.rememberUserName" label="记住用户名" size="large">
                                </el-checkbox>
                            </el-col>
                        </div>
                        <div class="line-item"></div>
                        <div>
                            <el-col :span="12">
                                <el-checkbox v-model="loginFormData.rememberPassword" label="记住密码" size="large">
                                </el-checkbox>
                            </el-col>
                        </div>
                    </div>

                    <el-form-item>
                        <el-button type="primary" @click="onSubmit(loginFormRef)">登录</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
        <div class="login-footer">
                版权:future
        </div>
    </div>
</template>

<script lang="ts" setup>
import { reactive, ref, watch,onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {instance as api} from "@/api/api"
import utils from "@/utils/utils"
const logoImage = new URL("@/assets/logo_3.png", import.meta.url).href
const loginText = ref("基于3DGS与WebGL的三维重建系统")
// const loginText = "信息管理系统"
const router = useRouter();

const loginFormData = reactive({
    username: '',
    password: '',
    rememberUserName:false,
    rememberPassword:false
})

const loginFormRef = ref({
    username: loginFormData.username,
    password: loginFormData.password,
})
const rules = reactive({
    username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
})
//用于提交

onMounted(()=>{
    loginFormData.username=utils.getData("username")
    loginFormData.password=utils.getData("password")
    loginFormData.rememberUserName=utils.getData("rememberUserName")
    loginFormData.rememberPassword=utils.getData("rememberPassword")
})
const onSubmit = (loginFormRef) => {
    let isOk=true;
    loginFormRef.validate((valid,fields)=>{
        if(!valid){
            isOk=false;
        }
    });
    if (!isOk) {
        return;
    }
    console.log(loginFormRef.value)
    utils.saveData("rememberUserName",loginFormData.rememberUserName)
    utils.saveData("rememberPassword",loginFormData.rememberPassword)

    if (loginFormData.rememberUserName) {
        utils.saveData("username",loginFormData.username)
    }else{
        utils.removeData("username")
    }
    if (loginFormData.rememberPassword) {
        // 明文存储 危险
        utils.saveData("password",loginFormData.password)
    }else{
        utils.removeData("password")
    }

        // 只需要 username 和 password 进行登录
    const loginData = {
        username: loginFormData.username,
        password: loginFormData.password
    };
    // 后台登陆
    api.post('/auth/login',new URLSearchParams(loginData),{
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }).then(response => {
            return response.data.token

        }).then(token=>{
            localStorage.setItem('token',token)
            // alert('登录成功')
            router.push('/home')
        }).catch(error => {
            alert('密码错误登录失败')
            console.log(error.response.data.detail)
    })
}
</script>

<style src="@/styles/loginView.css" scoped></style>