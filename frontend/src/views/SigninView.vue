<template>
  <BaseForm @submit.prevent="handleSubmit" button-text="Sign In" :disableButton="v$.$error || v$.$errors.length > 0">
    <BaseInput v-model="state.account" placeholder="Account" :hasError="v$.account.$error" :errors="v$.account.$errors"
      id="account" type="text" @blur="v$.account.$touch"></BaseInput>
    <BaseInput v-model="state.password" placeholder="Password" :hasError="v$.password.$error"
      :errors="v$.password.$errors" id="password" type="password" @blur="v$.password.$touch"></BaseInput>
  </BaseForm>
</template>

<script setup>
import { reactive, computed } from 'vue';
import useVuelidate from '@vuelidate/core';
import { required, alphaNum, helpers } from '@vuelidate/validators';
import { useRouter } from 'vue-router';
import axios from 'axios';
import BaseInput from '@/components/BaseInput.vue';
import BaseForm from '@/components/BaseForm.vue';
import { useUserStore } from '../stores/user';

const router = useRouter();
const store = useUserStore();

const state = reactive({
  account: '',
  password: '',
});

const isAccountExists = async () => {
  try {
    const response = await axios.get(`check/${state.account}`);
    return response.data.exists;
  } catch (error) {
    console.log(error);
    return true;
  }
}

const rules = computed(() => ({
  account: {
    required,
    alphaNum,
    accountExists: helpers.withMessage('Account does not exist', helpers.withAsync(isAccountExists)),
  },
  password: {
    required,
    alphaNum,
  },
}));

const v$ = useVuelidate(rules, state);

const handleSubmit = async () => {
  v$.value.$touch();

  if (v$.value.$error) {
    state.password = '';
    return;
  }

  try {
    const response = await axios.post('/login', { ...state });
    alert('Login successfully!');
    store.$state = response.data;
    router.push({ name: 'search' });
  } catch {
    alert('Login failed!');
    state.password = '';
  }
}
</script>

<style scoped lang="scss">
</style>
