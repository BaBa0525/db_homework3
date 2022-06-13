<template>
  <transition name="fade" appear>
    <div class="modal-overlay" v-if="show" @click="$emit('close-popup')"></div>
  </transition>
  <transition name="slide" appear>
    <div class="modal" v-if="show">
      <IconExitPopup class="icon" @click="$emit('close-popup')"></IconExitPopup>
      <slot></slot>
    </div>
  </transition>
</template>

<script setup>
import IconExitPopup from './icons/IconExitPopup.vue';

const props = defineProps({
  show: {
    Type: Boolean,
    default: false,
  },
});

const emits = defineEmits(['close-popup'])
</script>

<style lang="scss" scoped>
@import "@/styles/global.scss";

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 98;

  background-color: rgba(0, 0, 0, 0.3);
}

.modal {
  position: fixed;
  top: 15%;
  left: 15%;
  right: 15%;
  bottom: 15%;
  z-index: 99;
  padding: 50px;

  background-color: var(--white-color);
  border-radius: 16px;

  overflow-y: scroll;

  &::-webkit-scrollbar {
    display: none;
  }

  .icon {
    position: absolute;
    top: 25px;
    right: 25px;
  }

  @include flex;
  justify-content: flex-start;
  align-items: center;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.5s;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateY(100vh);
}
</style>