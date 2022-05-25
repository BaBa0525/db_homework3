<script setup lang="ts">
import { ref, computed, defineAsyncComponent } from 'vue';
import LoginPage from './components/LoginPage.vue';

enum ComponentIndex {
  loginPage,
  homePage,
};

const activeIndex = ref(ComponentIndex.loginPage);
const asyncHomePage = defineAsyncComponent(() => import('./components/HomePage.vue'));

const activeComponent = computed(() => {
  switch (activeIndex.value) {
    case ComponentIndex.loginPage: return LoginPage;
    case ComponentIndex.homePage: return asyncHomePage;
  }
});
</script>

<template>
  <h3 @click="activeIndex = ComponentIndex.loginPage">Login</h3>
  <h3 @click="activeIndex = ComponentIndex.homePage">Home</h3>
  <component :is="activeComponent" />
</template>

<style scoped lang="scss">
h3:hover {
  cursor: pointer;
}
</style>
