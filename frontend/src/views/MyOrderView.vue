<template>
    <BaseDropDown v-model="state.status" id='status' :options='options' />

    <BaseTable :fields="orderfields" :item="orders">
        <template #cell(detail)="{ item }">
            <button type="button" @click="showDetail(item)">Order Details</button>
        </template>
        <template #cell(action)="{ item }">
            <button type="button" :show="item.status === 'Not finished'" @click="cancelOrder(item)">Cancel</button>
        </template>
    </BaseTable>

    <PopupModal :show="popupDetail.active" @close-popup="popupDetail.active = false">
        <h1>Order</h1>
        <BaseTable :fields="popupFields" :items="getOrderDetail()"></BaseTable>
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

const state = reactive({
    status: 'All',
})

const options = ['All', 'Finished', 'Not Finished', 'cancel'];
const orderfields = [
    { key: 'OID', sortable: false },
    { key: 'status', sortable: false },
    { key: 'startTime', sortable: false },
    { key: 'endTime', sortable: false },
    { key: 'shopname', sortable: false },
    { key: 'subtotal', sortable: false },
    { key: 'detail', sortable: false },
    { key: 'action', sortable: false },
];

const orders = ref([]);

const userStore = useUserStore();

const popupDetail = reactive({
    active: false,
    order: [],
    orderDetail: [],
});

const showDetail = (item) => {
    popupDetail.active = true;
    popupDetail.order = item;
}

const cancelOrder = async (item) => {
    await axios.post('/cancelorder', {
        orderID: item.OID,
    });
    await loadOrders();
}

const loadOrders = async () => {
    try {
        const response = await axios.get(`/getorder/${userStore.account}`);
        orders.value = response.data;
    }
    catch (error) {
        console.log(error);
    }
}

const popupFields = [
    { key: 'picture', sortable: false },
    { key: 'mealname', sortable: false },
    { key: 'price', sortable: false },
    { key: 'quantity', sortable: false },
];

const getOrderDetail = async (item) => {
    try {
        const response = await axios.get(`/getorderdetail/${item.OID}`);
        popupDetail.orderDetail = response.data;
        return response.data;
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

<style>
</style>