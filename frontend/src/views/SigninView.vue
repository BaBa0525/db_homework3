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

const router = useRouter();

const state = reactive({
  account: '',
  password: '',
});

const isAccountExists = async () => {
  const response = await axios.get(`check/${state.account}`);
  return response.data.exists;
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
    state.password = state.confirm = '';
    return;
  }

  try {
    await axios.post('/login', { ...state });
    alert('Login successfully!');
    router.push({ name: 'home' });
  } catch {
    alert('Login failed!');
    state.password = state.confirm = '';
  }
}
</script>

<style scoped lang="scss">
</style>
