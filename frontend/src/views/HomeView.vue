<template>
  <div class="container">
    <SideBar></SideBar>
    <div class="view" :style="{ 'margin-left': `calc(${sidebarStore.sidebarWidth} + 2rem)`}">
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

.view{
    @include flex;
    justify-content: flex-start;
}
</style>
