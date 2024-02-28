import axios from "axios";
const instance = axios.create({
    baseURL:"http://192.168.31.17:8000"
})
const ossInstance = axios.create({
    baseURL:"http://192.168.31.17:8080"
})
export {instance, ossInstance};