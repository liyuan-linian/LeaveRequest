<template>
  <el-form :model="form" label-width="auto" style="max-width: 600px">

    <el-form-item label="用户名">
      <el-input v-model="form.name"/>
    </el-form-item>
    <el-form-item label="密码">
      <el-input v-model="form.password"/>
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="onSubmit">Create</el-button>
      <el-button>Cancel</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import {reactive} from 'vue'
import {login} from "../api/members.ts";
import { userStore } from '../store/modules/user';
import router from "../router";
// do not use same name with ref
const form = reactive({
  name: '',
  password: '',
})

const user = userStore()

const onSubmit = async () => {
  try {
    const respone = await login(form.name, form.password)
    if(respone.status === 200){
      const userInfo = respone.data.data
      user.setUser(userInfo)
      form.name = ""
      form.password = ""
      router.replace({name:"Login"})
    }
  }
  catch (error){
    alert(error)
  }
}
</script>
