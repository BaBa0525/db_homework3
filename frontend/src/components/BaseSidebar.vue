<template>
  <aside :class="asideClass(expand)">
    <IconLogo class="logo"></IconLogo>
    <div class="menu-toggle-wrap">
      <button class="menu-toggle" @click="toggleMenu">
        <IconToggle></IconToggle>
      </button>
    </div>
    <slot></slot>
  </aside>
</template>

<script setup>
import { computed } from 'vue';
import IconLogo from './icons/IconLogo.vue';
import IconToggle from './icons/IconToggle.vue';

const props = defineProps({
  expand: {
    type: Boolean,
    default: false,
  }
});

const asideClass = computed((isExpanded) => {
  if (isExpanded) return "expand";
  else return "shrink";
});
</script>

<style scoped lang="scss">
@import "@/styles/global.scss";

aside {
  display: flex;
  flex-direction: column;
  width: calc(2rem + 32px);
  padding: 1rem;
  overflow: hidden;
  min-height: 100vh;
  background-color: var(--secondary-color);
  color: var(--text-color);
  transition: 0.3s ease-in-out;

  .flex {
    flex: 1 1 0;
  }

  .logo {
    margin-bottom: 1rem;
  }

  .menu-toggle-wrap {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 1rem;
    position: relative;
    top: 0;
    transition: 0.3s ease-out;

    .menu-toggle {
      transition: 0.3s ease-out;

      &:hover {
        color: var(--info-color);
        transform: translateX(0.5rem);
      }
    }
  }

  h3,
  .button .text {
    opacity: 0;
    transition: 0.4s ease-out;
  }

  h3 {
    color: var(--lightgray-color);
    font-size: 0.8rem;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
  }

  .button .text {
    font-weight: 600;

    .profile-text {
      font-weight: 400;
    }
  }

  .menu {
    margin: 0 -1rem;

    .button {
      cursor: pointer;
      display: flex;
      align-items: center;
      text-decoration: none;
      padding: 0.5rem 1rem;
      transition: 0.3s ease-out;

      .icon {
        color: var(--text-color);
        transition: 0.3s ease-out;
      }

      .text {
        color: var(--text-color);
        transition: 0.3s ease-out;
      }

      &:hover,
      &.router-link-exact-active {
        background-color: var(--gray-color);

        .icon,
        .text {
          color: var(--info-color);
        }
      }

      &.router-link-exact-active {
        border-right: 5px solid var(--info-color);
      }
    }
  }

  .profile {
    margin: 0 -1rem;

    .button {
      display: flex;
      align-items: center;
      text-decoration: none;
      padding: 0.5rem 1rem;
      transition: 0.3s ease-out;

      .icon {
        color: var(--text-color);
        transition: 0.3s ease-out;
        cursor: pointer;
      }

      .text {
        color: var(--text-color);
        transition: 0.3s ease-out;
      }
    }

    form {
      @include flex-row;
      align-items: center;

      .location {
        @include flex;
        align-content: flex-start;

        .lat .lng {
          @include flex-row;
        }
      }

      input {
        border: 1px solid var(--secondary-color);
        outline: none;
        width: 50%;
        color: var(--text-color);
        background-color: var(--secondary-color);
        border-bottom: 1px solid var(--black-color);

        &:disabled {
          border: 1px solid var(--secondary-color);
        }
      }
    }

    .edit {
      cursor: pointer;
    }
  }

  &.expanded {
    width: 300px;

    .menu-toggle-wrap {
      top: -3rem;

      .menu-toggle {
        transform: rotate(-180deg);
      }
    }

    h3,
    .button .text {
      opacity: 1;
    }

    .button {
      .icon {
        margin-right: 1rem;
      }
    }
  }

  @media (max-width: 768px) {
    position: fixed;
    z-index: 99;
  }

  button {
    cursor: pointer;
    appearance: none;
    border: none;
    outline: none;
    background: none;
  }
}
</style>