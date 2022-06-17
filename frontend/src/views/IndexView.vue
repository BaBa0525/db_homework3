<template>
    <div class="index">
        <div class="container">
            <router-link class="router-link" to="/signin">Sign In</router-link>
            <router-link class="router-link" to="/signup">Sign Up</router-link>
        </div>
        <router-view></router-view>
    </div>
</template>

<script setup>
</script>

<style scoped lang="scss">
@import "@/styles/global.scss";

.index {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);

    .container {
        @include flex-row;
        width: clamp(300px, 30%, 400px);
        justify-content: space-between;

        .router-link {
            margin: 10px;
            text-decoration: none;
            color: var(--text-color);
            transition: 0.3s all ease;

            &:hover {
                font-size: 26px;
                color: var(--black-color);
            }
        }

        .router-link-exact-active {
            color: var(--black-color);
            font-size: 26px;
        }
    }
}
</style>
