<template>
  <div v-if="userStore.isOwner">
    <div class="base-container">
      <BaseDropDown v-model="state.status" id="status" :options="options" @choose="loadOrders" />

      <BaseTable :fields="orderfields" :items="orders">
        <template #cell(select)="{ item }">
            <input type="checkbox" v-if="item.status === 'Not finished'" v-model="item.checked" />
        </template>
        <template #cell(total_price)="{ item }">
          ${{ item.subtotal + item.deliverFee }}
        </template>
        <template #cell(detail)="{ item }">
          <button type="button" @click="showDetail(item)">Order Details</button>
        </template>
        <template #cell(action)="{ item }">
          <div class="button-flex">
            <button type="button" v-if="item.status === 'Not finished'" @click="finishOrder(item)">Finish</button>
            <button type="button" v-if="item.status === 'Not finished'" @click="cancelOrder(item)">Cancel</button>
          </div>
        </template>
      </BaseTable>
      <div class="button-flex">
        <button type="button" v-if="haschecked" @click="finishOrder()">finish</button>
        <button type="button" v-if="haschecked" @click="cancelOrder()">cancel</button>
      </div>
    </div>
    <PopupModal :show="popupDetail.active" titles="Order" @close-popup="popupDetail.active = false">
      <BaseTable :fields="popupFields" :items="popupDetail.orderDetail">
        <template #cell(picture)="{ item }">
          <BaseImage :src="item.image" :alt="item.mealname" width="100" height="100" />
        </template>
      </BaseTable>
      <div class="totalprice">
        <p>Subtotal ${{ subtotal }}</p>
        <p>Delivery Fee ${{ deliverFee }}</p>
        <hr>
        <p>Total Price ${{ subtotal + deliverFee }}</p>
      </div>
    </PopupModal>
  </div>
  <div class="container" v-else>
    <h1>You are not a shop owner!</h1>
    <img src="@/assets/powerman.png">
  </div>
</template>

<script setup>
import { reactive, computed, ref } from 'vue';
import { useUserStore } from '../stores/user';
import axios from 'axios';
import BaseDropDown from '../components/BaseDropDown.vue';
import BaseTable from '../components/BaseTable.vue';
import BaseImage from '../components/BaseImage.vue';
import PopupModal from "../components/PopupModal.vue";

const state = reactive({
  status: 'All',
})

const options = ['All', 'Finished', 'Not finished', 'Cancelled'];
const orderfields = [
  { key: 'select', sortable: false},
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
  await getOrderDetail();
  console.log(popupDetail.orderDetail);
}

const haschecked = computed(() => (orders.value.filter((food) => (food.checked)).length > 0))

const cancelOrder = async (item = null) => {   
  try{
    const checkedorder = orders.value.filter((food) => (food.checked)).map((order) => (order.OID));
    await axios.post('/cancelorder', {
      orderIDs: (item === null) ? checkedorder : [item.OID],
    });
    await loadOrders();
    alert("cancel successfully")
  } catch(error){
    alert(error.response.data.message);
  }
}

const loadOrders = async () => {
  try {
    const response = await axios.post('/getshoporder', {
      shopname: userStore.shopname,
      status: state.status,
    });

    orders.value = response.data;
    for(const order of orders.value){
      order.checked = false;
    }
  }
  catch (error) {
    console.log(error);
  }
};

loadOrders();

const popupFields = [
  { key: 'RID', sortable: false },
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

const finishOrder = async (item = null) => {
  try {
    const checkedorder = orders.value.filter((food) => (food.checked)).map((order) => (order.OID));
    await axios.post('/finishorder', {
    orderIDs: (item === null) ? checkedorder : [item.OID],
    })
    alert('Finish Order Successfully!');
  }
  catch {
    alert(error.response.data.message);
  }

  await loadOrders();
}

</script>

<style scoped lang="scss">
@import "@/styles/global.scss";

.container {
  @include flex;
  margin: auto;
  width: 75vh;

  h1 {
    margin: auto;
  }
}

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

.base-container {
  @include flex;
  align-items: flex-start;
}

.button-flex {
  @include flex-row;
  gap: 0.1rem;
}
</style>