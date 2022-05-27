<template>
  <router-view />
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import { useUserStore } from "./stores/user";

const store = useUserStore();
const router = useRouter();

if (store.isLoggedIn) router.push({ name: "home" });
else router.push({ name: "signin" });
</script>

<style lang="scss">
@import "@/styles/global.scss";

#app {
  @include flex;
  height: 100vh;
  width: 100vw;
  margin: 0;
  align-items: center;
  font-family: consolas;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
