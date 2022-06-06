<template>
  <router-view></router-view>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useUserStore } from './stores/user.js';

const router = useRouter();
const userStore = useUserStore();

router.push({ name: userStore.isLogin ? "home" : "index" });
</script>

<style lang="scss">
@import "@/styles/global.scss";

#app {
  @include flex;
  height: 100vh;
  width: 100vw;
  margin: 0;
  align-items: center;
  background-color: var(--primary-color);
  font-family: "Google Sans";
  font-family: Arial, Helvetica, sans-serif;
}
</style>
