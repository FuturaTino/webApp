<template>
    <div class="container">
        <form @submit.prevent="register">
            <div>
                <label for="username">用户:</label>
                <input type="text" id="username" v-model="form.username" required>
            </div>

            <div>
                <label for="password">密码:</label>
                <input type="password" id="password" v-model="form.password" required>
            </div>
            <div>
                <button type="submit">注册</button>
            </div>

        </form>
    </div>
</template>
<script setup>
import { ref } from 'vue';
import axios from "axios";
import {instance as api} from "@/api/api";
import {useRouter} from "vue-router"

const router = useRouter();
const form = ref({
    username: "",
    password: ""
})

const backToLogin = ()=>{
    router.push({name: "login"});
}

const register = () =>{
    const response = api.post("/auth/register", new URLSearchParams(form.value),
    {
        headers:{
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then(response=>{
        alert(`${response.data.user.username}，注册成功`);
        backToLogin();
    }).catch(error => {
        if (axios.isAxiosError(error)) {
            if (error.response && error.response.status === 400) {
                alert('用户名已被注册');
            } else {
                console.error(error.message);
            }
        } else {
            console.error('发生了一个错误');
        }
    });
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


</style>