import {createRouter, createWebHistory} from "vue-router";
import PersonInformation from "../components/PersonInformation.vue";
import Main from "../components/Main.vue";
import Login from "../components/Login.vue";

const Router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/PersonInformation', component: PersonInformation},
        {path: '/Main', component: Main},
        {path: '/Login', component: Login}
    ]
})

export default Router