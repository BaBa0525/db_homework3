<template>
    <BaseDropDown v-model="state.status" id='status' :options='options' />

    <BaseTable :fields="orderfields" :item="orders">
        <template #cell(detail)="{ item }">
            <button type="button" @click="showDetail(item)">Order Details</button>
        </template>
        <template #cell(action)="{ item }">
            <button type="button" @click="cancelOrder(item)">Cancel</button>
        </template>
    </BaseTable>

    <PopupModal :show="popupDetail.active" @close-popup="popupDetail.active = false">
        <h1>Order</h1>
        <BaseTable :fields="popupFields" :items="getOrderDetail()"></BaseTable>
        <div class="totalprice">
            <p>Subtotal ${{ subtotal }}</p>
            <p>Delivery Fee ${{ deliveryFee }}</p>
            <hr>
            <p>Total Price ${{ subtotal + deliveryFee }}</p>
        </div>
    </PopupModal>
</template>

<script setup>
import { reactive, computed } from 'vue';
import { useUserStore } from '../stores/user';
import BaseDropDown from '../components/BaseDropDown.vue';
import BaseTable from '../components/BaseTable.vue';
import PopupModal from "../components/PopupModal.vue";

const state = reactive({
    status: 'All',
})

const options = ['All', 'Finished', 'Not Finished', 'cancel'];
const orderfields = [
    { key: 'Order ID', sortable: false },
    { key: 'Status', sortable: false },
    { key: 'Start', sortable: false },
    { key: 'End', sortable: false },
    { key: 'Shop Name', sortable: false },
    { key: 'Total Price', sortable: false },
    { key: 'Order Details', sortable: false },
    { key: 'Action', sortable: false },
];

const orders = reactive([]);

const userStore = useUserStore();

const popupDetail = reactive({
    active: false,
    orderDetail: [],
});

const showDetail = (item) => {
    popupDetail.active = true;
    popupDetail.order = item;
}

const cancelOrder = (item) => {

}

const popupFields = [
    { key: 'Picture', sortable: false },
    { key: 'Meal Name', sortable: false },
    { key: 'Price', sortable: false },
    { key: 'Quantity', sortable: false },
];

const getOrderDetail = () => {

}

const subtotal = computed(() => {
    let total = 0;
});

const deliveryFee = computed(() => {

})

</script>

<style>
</style>