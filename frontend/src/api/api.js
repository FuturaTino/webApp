import axios from "axios";
const instance = axios.create({
    baseURL:"http://192.168.31.17:8000"
})

export default instance;