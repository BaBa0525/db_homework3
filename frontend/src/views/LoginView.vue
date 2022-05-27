<template>
  <div id="login">
    <div class="container">
      <router-link to="/signin" class="router-link">Sign In</router-link>
      <router-link to="/signup" class="router-link">Sign Up</router-link>
    </div>
    <router-view />
  </div>
</template>

<script setup lang="ts"></script>

<style scoped lang="scss">
@import "@/styles/global.scss";

#login {
  align-self: center;
  .container {
    @include flex-row;
    justify-content: space-between;

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
  }
}
</style>
