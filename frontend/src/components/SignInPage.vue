<template>
  <h1>This is Sign In Page</h1>
  <form @submit.prevent="handleSubmit" class="beautiful-form">
    <div class="input">
      <input v-model.lazy="state.account" type="text" id="account" :class="getInputClass('account')"
        @blur="v$.account.$touch" />
      <label for="account" class="placeholder">
        <span>Account</span>
      </label>
      <ul v-if="v$.account.$error">
        <li v-for="(error, index) in v$.account.$errors" :key="index">
          {{ error.$message }}
        </li>
      </ul>
    </div>
    <div class="input">
      <input v-model.lazy="state.password" id="password" type="password" :class="getInputClass('password')"
        @blur="v$.password.$touch" />
      <label for="password" class="placeholder">
        <span>Password</span>
      </label>
      <ul v-if="v$.password.$error">
        <li v-for="(error, index) in v$.password.$errors" :key="index">
          {{ error.$message }}
        </li>
      </ul>
    </div>
    <button type="submit">Login</button>
  </form>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
import useVuelidate from '@vuelidate/core';
import { required, helpers } from '@vuelidate/validators';
import axios from 'axios';
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();
const state = reactive({
  account: '',
  password: ''
});

const { withAsync } = helpers;

const accountValidation = withAsync(async (value: string) => {
  try { await axios.get(`getuser/${value}`); }
  catch (error) {
    console.log(error);
    return false;
  }
  console.log('No Error');
  return true;
});

const rules = {
  account: { required, checkAccount: helpers.withMessage('Account does not exist.', accountValidation) },
  password: { required },
};

const v$ = useVuelidate(rules, state);

async function handleSubmit() {
  const isFormCorrect = await v$.value.$validate();
  if (!isFormCorrect) return;

  try {
    const response = await axios.post("login", {
      account: state.account,
      password: state.password
    });
    console.log(response.data);
    userStore.setUser(response.data as User);
  }
  catch (error) {
    alert("Login failed");
    state.password = '';
    return;
  }
}

function getInputClass(field: string) {
  if (field !== 'account' && field !== 'password') return;
  return (v$.value[field].$error ? "danger" : "") + (state[field] ? " filled" : "");
}
</script>

<style scoped lang="scss">
</style>