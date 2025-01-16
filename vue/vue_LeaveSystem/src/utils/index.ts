import axios from "axios";

var URL = 'http://localhost:8080/'

const service = axios.create({
    baseURL: URL,
    timeout: 60000,
    responseType: 'json',
    headers: {
        "Content-Type": "application/json;charset=utf-8", //数据格式类型
        "Access-Control_Allow-Origin": "*", //允许跨域
    },
})


export default service