<template>
<div class="container">
    <IconProfile></IconProfile> <br/>

<ul>
    <li>account: {{userStore.account}} </li>
    <li>phone number: {{userStore.phone}}</li>
    <li>location: {{userStore.latitude}}, {{userStore.longitude}}</li>
    <button>Change location</button>
    <li>wallet balance: $100{{userStore.balance}}</li>
    <button>Recharge</button>
</ul>
</div>

</template>

<script setup>
import { useUserStore } from '../stores/user';
import IconProfile from '../components/icons/IconProfile.vue';

const userStore = useUserStore();

</script>

<style scoped lang="scss">
@import "@/styles/global.scss";

.container{
    @include flex;
    justify-content: center;
    align-items: center;

    ul {
        list-style: none;
        font-size: 2rem;
        font-weight: 600;
        li {
            margin-top: 1rem;
        }
    }

    button {
        border: none;
        border-radius: 4px;
        padding: 10px 12px;
        margin-top: 1rem;
        background-color: var(--info-color);
        color: var(--white-color);
        cursor: pointer;
        transition: all 0.3s ease;

        &:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
    }
}

</style>