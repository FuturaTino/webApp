<template>
    <div class="container">
        <form @submit.prevent="login">
            <div>
                <label for="username">用户:</label>
                <input type="text" id="username" v-model="form.username">
            </div>
            <div>
                <label for="password">密码:</label>
                <input type="password" id="password" v-model="form.password">
            </div>
            <div class="button-group">
                <button type="submit">登录</button>
                <button id="register">注册</button>
            </div>

        </form>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import {instance as api} from "@/api/api"

const router = useRouter();
const form = ref({
    username: '',
    password: ''
})
watch(form, () => {
    console.log(form.value)
})


const login = () => {api.post('/auth/login',new URLSearchParams(form.value),{
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

<style scoped>
form {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
}
form div {
    margin: 10px;
}

form div label {
    margin-right: 5px;
}
.button-group {
    display: flex;
    flex-direction: row;
}
.button-group button {
    margin:5px;
}
</style>