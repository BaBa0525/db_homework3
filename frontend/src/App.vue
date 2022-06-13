<template>
  <router-view></router-view>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useUserStore } from './stores/user.js';

const router = useRouter();
const userStore = useUserStore();

router.push({ name: userStore.isLogin ? 'search' : 'signin' });
</script>

<style lang='scss'>
@import '@/styles/global.scss';

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  width: 100vw;
}
</style>
