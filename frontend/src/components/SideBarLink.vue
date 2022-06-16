<template>
<router-link :to="to" class="link" :class="{'active': isActive}">
<component :is="icon" class="icon"></component>
<transition name="fade">
  <slot v-if="!sidebarStore.collapsed"></slot>
</transition>
</router-link>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { useSidebarStore } from "../stores/sidebar"

const props = defineProps({
    to:{type: String, required: true},
    icon: {type: Object, required: true}
});


const sidebarStore = useSidebarStore()
const route = useRoute()
const isActive = computed(() => route.path === props.to)
</script>


<style scoped lang="scss">

.fade-enter-active,
.fade-leave-active {
  transition: opacity 5s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.link {
  display: flex;
  align-items: center;
  cursor: pointer;
  position: relative;
  font-weight: 400;
  user-select: none;
  margin: 0.1em 0;
  padding: 0.4em;
  border-radius: 0.25em;
  height: 1.5em;
  color: white;
  text-decoration: none;

  &:hover {
    background-color: var(--sidebar-item-hover);
  }

  &.active {
    background-color: var(--sidebar-item-active);
  }

  .icon {
  flex-shrink: 0;
  width: 25px;
  margin-right: 10px;
  }
}
</style>