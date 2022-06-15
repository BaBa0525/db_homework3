<template>
    <router-link to="search"> Search </router-link>
    <router-link to="shop"> Shop </router-link>
    <button @click="userStore.logout"> Logout </button>
    <router-view></router-view>

</template>

<script setup>
import { useUserStore } from '../stores/user';

const userStore = useUserStore();
</script>

<style scoped>
</style>
