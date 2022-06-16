<template>
  <transition name="fade" appear>
    <div class="modal-overlay" v-if="show" @click="$emit('close-popup')"></div>
  </transition>
  <transition name="slide" appear>
    <div class="modal" v-if="show">
      <IconExitPopup class="icon" @click="$emit('close-popup')"></IconExitPopup>
      <h1>{{titles}}</h1>
      <hr/>
      <slot></slot>
    </div>
  </transition>
</template>

<script setup>
import IconExitPopup from './icons/IconExitPopup.vue';

const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  titles: {
    type: String,
    default: '',
  }
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

  overflow-y: auto;
  scrollbar-gutter: stable;

  h1{
    align-self: flex-start;
    transform: translateY(-50%);
  }

  hr{
    width: 100%;
    border: 2px solid gray;
    transform: translateY(-2rem);
  }

  &::-webkit-scrollbar {
    width: 16px;
  }

  &::-webkit-scrollbar-track {
    background-color: #e4e4e4;
    border-radius: 100px;
  }

  &::-webkit-scrollbar-thumb {
    border: 5px solid transparent;
    border-radius: 100px;
    background-color: darkgray;

    &:hover {
      background-color: gray;
    }

    background-clip: content-box;
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