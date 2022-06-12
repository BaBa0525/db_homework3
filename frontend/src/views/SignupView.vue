<template>
    <BaseForm @submit.prevent="handleSubmit" button-text="Sign Up" :disableButton="v$.$error || v$.$errors.length > 0">
        <BaseInput v-model="state.realname" placeholder="Real Name" :hasError="v$.realname.$error"
            :errors="v$.realname.$errors" id="realname" type="text" @blur="v$.realname.$touch"></BaseInput>
        <BaseInput v-model="state.account" placeholder="Account" :hasError="v$.account.$error"
            :errors="v$.account.$errors" id="account" type="text" @blur="v$.account.$touch"></BaseInput>
        <BaseInput v-model="state.phone" placeholder="Phone Number" :hasError="v$.phone.$error"
            :errors="v$.phone.$errors" id="phone" type="text" @blur="v$.phone.$touch"></BaseInput>
        <BaseInput v-model="state.password" placeholder="Password" :hasError="v$.password.$error"
            :errors="v$.password.$errors" id="password" type="password" @blur="v$.password.$touch"></BaseInput>
        <BaseInput v-model="state.confirm" placeholder="Confirm Password" :hasError="v$.confirm.$error"
            :errors="v$.confirm.$errors" id="confirm" type="password" @blur="v$.confirm.$touch"></BaseInput>
        <BaseInput v-model="state.latitude" placeholder="Latitude" :hasError="v$.latitude.$error"
            :errors="v$.latitude.$errors" id="latitude" type="text" @blur="v$.latitude.$touch"></BaseInput>
        <BaseInput v-model="state.longitude" placeholder="Longitude" :hasError="v$.longitude.$error"
            :errors="v$.longitude.$errors" id="longitude" type="text" @blur="v$.longitude.$touch"></BaseInput>
    </BaseForm>
</template>

<script setup>
import { reactive, computed } from 'vue';
import useVuelidate from '@vuelidate/core';
import { required, sameAs, numeric, between, helpers, alphaNum, alpha, and, not } from '@vuelidate/validators';
import BaseForm from '@/components/BaseForm.vue';
import BaseInput from '@/components/BaseInput.vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();

const state = reactive({
    realname: '',
    account: '',
    phone: '',
    password: '',
    confirm: '',
    latitude: '',
    longitude: '',
});

const isAccountUnique = async () => {
    const response = await axios.get(`check/${state.account}`);
    return !response.data.exists;
}

const rules = computed(() => ({
    realname: {
        required,
        alpha,
    },
    account: {
        required,
        alphaNum,
        uniqueAccount: helpers.withMessage('This account has been registered', helpers.withAsync(isAccountUnique)),
    },
    phone: {
        required,
        phoneFormat: helpers.withMessage('Invalid phone number', helpers.regex(/^09\d{8}$/)),
    },
    password: {
        required,
        alphaNum,
    },
    confirm: {
        required,
        alphaNum,
        sameAsPassword: helpers.withMessage('Please check your password again', sameAs(state.password)),
    },
    latitude: {
        required,
        possibleValue: helpers.withMessage('Invalid latitude', and(numeric, between(-90, 90))),
    },
    longitude: {
        required,
        possibleValue: helpers.withMessage('Invalid longitude', and(numeric, between(-180, 180))),
    },
}));

const v$ = useVuelidate(rules, state);

const handleSubmit = async () => {
    v$.value.$touch();

    if (v$.value.$error) {
        state.password = state.confirm = '';
        return;
    }

    try {
        await axios.post('/register', { ...state });
        alert('Registration succeed!');
        router.push({ name: 'signin' });
    } catch (error) {
        alert('Registration failed!');
        console.log(error);
        state.password = state.confirm = '';
    }
}
</script>

<style scoped lang="scss">
</style>
