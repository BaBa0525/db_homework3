<template>
    <router-link to="/signin" class="router-link">Sign In</router-link>
    <router-link to="/signup" class="router-link">Sign Up</router-link>
    <router-view></router-view>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();
</script>

<style scoped lang="scss">
.router-link {
    font-size: 20px;
    color: gray;
    text-decoration: none;
    transition: 0.3s all ease;

    &:hover {
        color: black;
        font-size: 30px;
    }
}

.router-link-exact-active {
    color: black;
    text-decoration: none;
    font-size: 26px;

    &:hover {
        font-size: 26px;
    }
}
</style>
