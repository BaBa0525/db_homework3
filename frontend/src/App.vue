<template>
  <div id="app">
    <h1>App</h1>
    <BaseInput
      id="account"
      v-model.lazy="state.form.account"
      placeholder="Account"
      :has-error="v$.form.account.$error"
      :errors="v$.form.account.$errors"
      type="text"
      @blur="v$.form.account.$touch"
    />
    <BaseInput
      id="password"
      v-model="state.form.password"
      placeholder="Password"
      :has-error="v$.form.password.$error"
      :errors="v$.form.password.$errors"
      type="password"
      @blur="v$.form.password.$touch"
    />
  </div>
</template>

<script setup>
import { reactive } from "vue";
import useVuelidate from "@vuelidate/core";
import { required } from "@vuelidate/validators";
import BaseInput from "./components/BaseInput.vue";

const state = reactive({
  form: {
    account: "",
    password: "",
  },
});

const rules = {
  form: {
    account: { required },
    password: { required },
  },
};

const v$ = useVuelidate(rules, state);
</script>

<style lang="scss">
@import "@/styles/global.scss";

#app {
  @include flex;
  height: 100vh;
  width: 100vw;
  margin: 0;
  align-items: center;
  background-color: var(--primary-color);
  font-family: "Google Sans";
  font-family: Arial, Helvetica, sans-serif;
}
</style>
