<template>
    <!-- <router-link to="search"> Search </router-link>
    <router-link to="shop"> Shop </router-link>
    <button @click="userStore.logout"> Logout </button> -->
    <SideBar></SideBar>
    <div :style="{ 'margin-left': sidebarStore.sidebarWidth}">
        <router-view></router-view>
    </div>

</template>

<script setup>
import { useUserStore } from '../stores/user';
import { useSidebarStore } from "../stores/sidebar"
import SideBar from '../components/SideBar.vue';

const userStore = useUserStore();
const sidebarStore = useSidebarStore()
</script>

<style scoped>
</style>
