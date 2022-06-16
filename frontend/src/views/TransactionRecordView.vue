<template>
    <BaseDropDown v-model="state.action" id="action" :options="options" />
    <BaseTable :fields="fields" :items="state.transaction"></BaseTable>
</template>

<script setup>
import { reactive, computed } from 'vue';
import { useUserStore } from '../stores/user';
import axios from 'axios';
import BaseDropDown from '../components/BaseDropDown.vue';
import BaseTable from '../components/BaseTable.vue';

const state = reactive({
    action: 'All',
    transaction: [],
})

const options = ['All', 'Payment', 'Recharge', 'Receive'];
const fields = [
    { key: 'Record ID', sortable: false },
    { key: 'Action', sortable: false },
    { key: 'Time', sortable: false },
    { key: 'Trader', sortable: false },
    { key: 'Amount change', sortable: false },
]

</script>

<style>
</style>