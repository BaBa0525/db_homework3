<template>
    <div class="popup">
        <div class="popup-inner">
            <IconExitPopup @click="$emit('exitPopup')" />
            <slot></slot>
        </div>
    </div>
</template>

<script setup>
import IconExitPopup from './icons/IconExitPopup.vue';
</script>

<style lang="scss" scoped>
@import "@/styles/global.scss";

.popup {
    @include flex;
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 99;
    background-color: rgba(0, 0, 0, 0.2);

    .popup-inner {
        background: var(--white-color);
        padding: 32px;
        margin: 20%;
        border-radius: 8px;
    }
}
</style>