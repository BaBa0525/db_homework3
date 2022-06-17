<template>
  <BaseDropDown v-model="state.status" id="status" :options="options" @choose="loadOrders" />

  <BaseTable :fields="orderfields" :items="orders">
    <template #cell(total_price)="{ item }">
      $ {{ item.subtotal + item.deliverFee }}
    </template>
    <template #cell(detail)="{ item }">
      <button type="button" @click="showDetail(item)">Order Details</button>
    </template>
    <template #cell(action)="{ item }">
      <button type="button" v-if="item.status === 'Not finished'" @click="cancelOrder(item)">Cancel</button>
    </template>
  </BaseTable>

  <PopupModal :show="popupDetail.active" titles="Order" @close-popup="popupDetail.active = false">

    <BaseTable :fields="popupFields" :items="popupDetail.orderDetail">
      <template #cell(picture)="{ item }">
        <BaseImage :src="item.image" :alt="item.name" width="100" height="100"></BaseImage>
      </template>
    </BaseTable>
    <div class="totalprice">
      <p>Subtotal ${{ subtotal }}</p>
      <p>Delivery Fee ${{ deliverFee }}</p>
      <hr>
      <p>Total Price ${{ subtotal + deliverFee }}</p>
    </div>
  </PopupModal>
</template>

<script setup>
import { reactive, computed, ref } from 'vue';
import { useUserStore } from '../stores/user';
import axios from 'axios';
import BaseDropDown from '../components/BaseDropDown.vue';
import BaseTable from '../components/BaseTable.vue';
import PopupModal from "../components/PopupModal.vue";
import BaseImage from '../components/BaseImage.vue';

const state = reactive({
  status: 'All',
})

const options = ['All', 'Finished', 'Not finished', 'Cancelled'];
const orderfields = [
  { key: 'OID', sortable: false },
  { key: 'status', sortable: false },
  { key: 'startTime', sortable: false },
  { key: 'endTime', sortable: false },
  { key: 'shopname', sortable: false },
  { key: 'total_price', sortable: false },
  { key: 'detail', sortable: false },
  { key: 'action', sortable: false },
];

const orders = ref([]);

const userStore = useUserStore();

const popupDetail = reactive({
  active: false,
  order: null,
  orderDetail: [],
});

const showDetail = async (item) => {
  popupDetail.active = true;
  popupDetail.order = item;
  console.log(popupDetail.order);
  await getOrderDetail();
}

const cancelOrder = async (item) => {
  await axios.post('/cancelorder', {
    orderIDs: [item.OID],
  });
  await loadOrders();
}

const loadOrders = async () => {
  try {
    const response = await axios.post('/getorder', {
      account: userStore.account,
      status: state.status,
    });

    orders.value = response.data;
  }
  catch (error) {
    console.log(error);
  }
}

loadOrders();

const popupFields = [
  { key: 'picture', sortable: false },
  { key: 'mealname', sortable: false },
  { key: 'price', sortable: false },
  { key: 'quantity', sortable: false },
];

const getOrderDetail = async () => {
  try {
    const response = await axios.get(`/getorderdetail/${popupDetail.order.OID}`);
    popupDetail.orderDetail = response.data;
    console.log(popupDetail.orderDetail);
  }
  catch (error) {
    console.log(error);
  }
}

const subtotal = computed(() => {
  return popupDetail.order.subtotal;
});

const deliverFee = computed(() => {
  return popupDetail.order.deliverFee;
})

</script>

<style scoped lang="scss">
@import "@/styles/global.scss";

button {
  border: none;
  border-radius: 4px;
  padding: 10px 12px;
  background-color: var(--info-color);
  color: var(--white-color);
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100px;

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.container {
  @include flex;
  align-items: flex-start;
}
</style>