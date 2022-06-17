<template>
  <div class="container">
    <BaseDropDown v-model="state.action" id="action" :options="options" @change="loadTransactions" />
    <BaseTable :fields="fields" :items="state.transaction">
      <template #cell(amount_change)="{ item }">
        {{ item.amount }}
      </template>
      <template #cell(record_ID)="{ item }">
        {{ item.RID }}
      </template>
    </BaseTable>
  </div>
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
  { key: 'record_ID', sortable: false },
  { key: 'action', sortable: false },
  { key: 'time', sortable: false },
  { key: 'trader', sortable: false },
  { key: 'amount_change', sortable: false },
]

const userStore = useUserStore();


const loadTransactions = async () => {
  try {
    const response = await axios.post('/transaction', {
      account: userStore.account,
      action: state.action,
    });
    state.transaction = response.data;

  } catch (error) {
    console.log(error);
  }
}
loadTransactions()

</script>

<style scoped lang="scss">
@import '../styles/global.scss';

.container {
  @include flex;

  align-items: flex-start;
}
</style>