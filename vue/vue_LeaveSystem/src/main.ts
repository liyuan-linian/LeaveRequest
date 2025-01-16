import { createApp } from 'vue'
import {createPinia} from "pinia";
import './style.css'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import Router from "./router";
import App from './App.vue'
//这里采用了全部导入的方式 考虑到项目体积 可以采用按需导入的方式

const app = createApp(App)
const pinia = createPinia()
app.use(Router).use(ElementPlus).use(pinia)
app.mount('#app')

