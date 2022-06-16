<template>
  <div class="container">
    <SideBar></SideBar>
    <div :style="{ 'margin-left': sidebarStore.sidebarWidth }">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '../stores/user';
import { useSidebarStore } from "../stores/sidebar"
import SideBar from '../components/SideBar.vue';

const userStore = useUserStore();
const sidebarStore = useSidebarStore()
</script>

<style scoped lang="scss">
@import "@/styles/global.scss";

.container {
  @include flex;

}
</style>
