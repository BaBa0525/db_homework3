<template>
<div class="container">
    <IconHead/> <br/>

<ul>
    <li>account: {{userStore.account}} </li>
    <li>phone number: {{userStore.phone}}</li>
    <li>location: {{userStore.latitude}}, {{userStore.longitude}}</li>
    <button @click="active.location = true">Change location</button>
    <li>wallet balance: ${{userStore.balance}}</li>
    <button @click="active.balance = true">Recharge</button>
</ul>
    <PopupModal :show="active.location" @close-popup="closePopup">
    <ul>
        <li>Current latitude: {{userStore.latitude}}</li>
        <li>Current longitude: {{userStore.longitude}}</li>
    </ul>
        <BaseInput v-model="location_state.newLatitude" placeholder="new latitude" :hasError="v_location$.newLatitude.$error"
      :errors="v_location$.newLatitude.$errors" id="newLatitude" type="text" @blur="v_location$.newLatitude.$touch" />
        <br/>
        <BaseInput v-model="location_state.newLongitude" placeholder="new longitude" :hasError="v_location$.newLongitude.$error"
      :errors="v_location$.newLongitude.$errors" id="newLongitude" type="text" @blur="v_location$.newLongitude.$touch" />
        <button @click="handleLocation">Update</button>
    </PopupModal>

    <PopupModal :show="active.balance" @close-popup="closePopup">
        <h1>Current balence: {{userStore.balance}}</h1>
        <BaseInput v-model="balance_state.addValue" placeholder="enter add value" :hasError="v_balance$.addValue.$error"
      :errors="v_balance$.addValue.$errors" id="addValue" type="text" @blur="v_balance$.addValue.$touch" />
        <button @click="handleRecharge">Charge</button>
    </PopupModal>
</div>

</template>

<script setup>
import { ref, reactive,computed } from 'vue';
import useVuelidate from '@vuelidate/core';
import { required, decimal, minValue, maxValue } from '@vuelidate/validators';
import { useUserStore } from '../stores/user';
import IconHead from '../components/icons/IconHead.vue'
import PopupModal from '../components/PopupModal.vue';
import BaseInput from '../components/BaseInput.vue';
import axios from 'axios';

const userStore = useUserStore();
const active = reactive({
    location: false,
    balance: false,
});

const balance_state = reactive({
    addValue: '',
});

const location_state = reactive({
    newLatitude: '',
    newLongitude: ''
});


const balance_rules = computed(() => ({
    addValue: {
        required,
        decimal,
        nonNegative: minValue(0),
        // nonNegative: helpers.withMessage('baba', minValue(0)),
    }
}));

const location_rules = computed(() => ({
    newLatitude: {
        required,
        decimal,
        minValue: minValue(-90),
        maxValue: maxValue(90),
        // nonNegative: helpers.withMessage('baba', minValue(0)),
    },
    newLongitude: {
        required,
        decimal,
        minValue: minValue(-180),
        maxValue: maxValue(180),
        // nonNegative: helpers.withMessage('baba', minValue(0)),
    }
}));

const v_balance$ = useVuelidate(balance_rules, balance_state);
const v_location$ = useVuelidate(location_rules, location_state);


const closePopup = () => {
    active.location = false;
    active.balance = false;
    balance_state.addValue = '';
    location_state.newLatitude = '';
    location_state.newLongitude = '';
    v_balance$.value.$reset();
    v_location$.value.$reset();
}

const handleLocation = async () => {
  try {

    await axios.put('/location', {
        account: userStore.account,
        latitude: location_state.newLatitude,
        longitude: location_state.newLongitude
    });
    
    await userStore.reload();
    alert('Recharge succeed!');

  } catch (error) {
    console.log(error);
    alert('Recharge fail!');
  }
  closePopup();
}

const handleRecharge = async () => {
  try {

    await axios.patch('/recharge', {
        account: userStore.account,
        value: balance_state.addValue
    });
    
    await userStore.reload();
    alert('Recharge succeed!');

  } catch (error) {
    console.log(error);
    alert('Recharge fail!');
  }
  closePopup();
}
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