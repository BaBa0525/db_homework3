<template>
  <div class="sidebar" :style="{ width: sidebarStore.sidebarWidth }">
    <h1>
      <span v-if="sidebarStore.collapsed">
        <div>F</div>
        <div>E</div>
      </span>
      <span v-else>Foober<br />Eats</span>
    </h1>
    <SideBarLink to="/profile" :icon="IconLogout">profile</SideBarLink>
    <SideBarLink to="/search" :icon="IconSearch">Search</SideBarLink>
    <SideBarLink to="/shop" :icon="IconShop">Shop</SideBarLink>
    <SideBarLink to="/myorder" :icon="IconMyorder">My Order</SideBarLink>
    <SideBarLink to="/shoporder" :icon="IconShoporder">Shop Order</SideBarLink>
    <SideBarLink to="/transaction" :icon="Transaction">Transaction Record</SideBarLink>
    <SideBarLink to="/signin" :icon="IconLogout" @click="userStore.logout">Logout</SideBarLink>

    <IconToggle class="toggle" :class="{ 'rotate-180': !sidebarStore.collapsed }" @click="sidebarStore.toggle" />

  </div>

</template>

<script setup>
import { useSidebarStore } from "../stores/sidebar"
import { useUserStore } from '../stores/user';
import IconToggle from "./icons/IconToggle.vue";
import IconSearch from "./icons/IconSearch.vue"
import IconShop from "./icons/IconShop.vue"
import IconMyorder from "./icons/IconMyorder.vue"
import IconShoporder from "./icons/IconShoporder.vue"
import Transaction from "./icons/IconTransaction.vue"
import SideBarLink from "./SideBarLink.vue";
import IconLogout from "./icons/IconLogout.vue"

const userStore = useUserStore();
const sidebarStore = useSidebarStore()
</script>



<style scoped lang="scss">
.sidebar {
  color: rgb(255, 255, 255);
  background-color: var(--sidebar-bg-color);
  float: left;
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  bottom: 0;
  padding: 0.5em;
  transition: 0.5s ease;
  display: flex;
  flex-direction: column;

  h1 {
    margin-left: 0.5rem;
    cursor: default;
  }

  .toggle {
    position: absolute;
    bottom: 0;
    padding: 0.75em;

    color: rgba(255, 255, 255, 0.7);

    transition: 0.2s linear;

    &.rotate-180 {
      transform: rotate(180deg);
      transition: 0.2s linear;
    }
  }

}
</style>
