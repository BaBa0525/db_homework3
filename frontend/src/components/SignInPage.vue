<template>
  <div>
    <form @submit.prevent="handleSubmit" class="beautiful-form">
      <div class="input">
        <input
          v-model.lazy="state.account"
          type="text"
          id="account"
          :class="getInputClass('account')"
          @blur="v$.account.$touch"
        />
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
        <input
          v-model.lazy="state.password"
          id="password"
          type="password"
          :class="getInputClass('password')"
          @blur="v$.password.$touch"
        />
        <label for="password" class="placeholder">
          <span>Password</span>
        </label>
        <ul v-if="v$.password.$error">
          <li v-for="(error, index) in v$.password.$errors" :key="index">
            {{ error.$message }}
          </li>
        </ul>
      </div>
      <button type="submit" :disabled="v$.$error">Login</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import useVuelidate from "@vuelidate/core";
import axios from "axios";
import { reactive } from "vue";
import { required, helpers } from "@vuelidate/validators";
import { useUserStore } from "../stores/user";
import type { User } from "../types/typeUser";

const userStore = useUserStore();

const state = reactive({
  account: "",
  password: "",
});

const accountValidation = helpers.withAsync(async (value: string) => {
  if (value.length === 0) return true;
  try {
    await axios.get(`/getuser/${value}`);
  } catch (error) {
    return false;
  }
  return true;
});

const rules = {
  account: {
    required,
    checkAccount: helpers.withMessage(
      "Account does not exist.",
      accountValidation
    ),
  },
  password: { required },
};

const v$ = useVuelidate(rules, state);

async function handleSubmit() {
  const isFormCorrect = await v$.value.$validate();
  if (!isFormCorrect) return;

  try {
    const response = await axios.post("/login", {
      account: state.account,
      password: state.password,
    });
    console.log(response.data);
    userStore.setUser(response.data as User);
  } catch (error) {
    alert("Login failed");
    state.password = "";
    return;
  }
}

function getInputClass<Key extends keyof typeof state>(field: Key) {
  return (
    (v$.value[field].$error ? "danger" : "") + (state[field] ? " filled" : "")
  );
}
</script>

<style scoped lang="scss"></style>
