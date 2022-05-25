<template>
  <router-view />
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useUserStore } from "@/stores/user";

const store = useUserStore();
const router = useRouter();

if (store.isLoggedIn) router.push({ name: 'home' });
else router.push({ name: 'signin' });
</script>

<style lang="scss">
@import "@/styles/global.scss";
</style>
