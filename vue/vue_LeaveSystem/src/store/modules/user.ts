import {defineStore} from "pinia";
import type {UserInfo} from "../types/user";

const DEFAULT_USER = "admin"
export const userStore = defineStore("User", {
    state: (): UserInfo => {
        const localData = localStorage.getItem(DEFAULT_USER)
        const defaultValue: UserInfo = {
            id: "",
            name: "",
            token: "",
        }
        return localData ? JSON.parse(localData) : defaultValue
    },
    getters: {
        getId(state: UserInfo): string {
            return state.id
        },
        getName(state: UserInfo): string {
            return state.name
        },
        getToken(state: UserInfo): string {
            return state.token
        },
        isLogin(state: UserInfo): boolean {
            return state.token != ""
        }
    },
    actions: {
        setUser(userDate: UserInfo): void {
            this.id = userDate.id;
            this.name = userDate.name;
            this.token = userDate.token;
            localStorage.setItem(DEFAULT_USER, JSON.stringify(userDate));
        },
    }
})