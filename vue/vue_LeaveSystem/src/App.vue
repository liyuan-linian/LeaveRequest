<script setup lang="ts">

</script>

<template>
<div>
  <div>
    <RouterLink to="/PersonInformation"> 个人中心 </RouterLink>
    <RouterLink to="/Main"> 请假展示 </RouterLink>
    <RouterLink to="/Login">登录</RouterLink>
  </div>
  <div>
    <RouterView></RouterView>
  </div>
</div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
