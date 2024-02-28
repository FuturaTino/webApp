import axios from "axios";
const instance = axios.create({
    baseURL:"http://192.168.31.17:8000" // 调度服务器接口地址
})
const ossInstance = axios.create({
    baseURL:"http://192.168.31.17:8080" // 阿里云oss签名服务器接口地址
})
export {instance, ossInstance};