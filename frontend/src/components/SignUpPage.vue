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
      <div class="input">
        <input
          v-model.lazy="state.confirm"
          id="confirm"
          type="password"
          :class="getInputClass('confirm')"
          @blur="v$.confirm.$touch"
        />
        <label for="confirm" class="placeholder">
          <span>Confirm Password</span>
        </label>
        <ul v-if="v$.confirm.$error">
          <li v-for="(error, index) in v$.confirm.$errors" :key="index">
            {{ error.$message }}
          </li>
        </ul>
      </div>
      <div class="input">
        <input
          v-model.lazy="state.name"
          id="name"
          type="text"
          :class="getInputClass('name')"
          @blur="v$.name.$touch"
        />
        <label for="name" class="placeholder">
          <span>Real Name</span>
        </label>
        <ul v-if="v$.name.$error">
          <li v-for="(error, index) in v$.name.$errors" :key="index">
            {{ error.$message }}
          </li>
        </ul>
      </div>
      <div class="input">
        <input
          v-model.lazy="state.phone"
          id="phone"
          type="text"
          :class="getInputClass('phone')"
          @blur="v$.phone.$touch"
        />
        <label for="phone" class="placeholder">
          <span>Phone Number</span>
        </label>
        <ul v-if="v$.phone.$error">
          <li v-for="(error, index) in v$.phone.$errors" :key="index">
            {{ error.$message }}
          </li>
        </ul>
      </div>
      <div class="input">
        <input
          v-model.lazy="state.latitude"
          id="latitude"
          type="text"
          :class="getInputClass('latitude')"
          @blur="v$.latitude.$touch"
        />
        <label for="latitude" class="placeholder">
          <span>Latitude</span>
        </label>
        <ul v-if="v$.latitude.$error">
          <li v-for="(error, index) in v$.latitude.$errors" :key="index">
            {{ error.$message }}
          </li>
        </ul>
      </div>
      <div class="input">
        <input
          v-model.lazy="state.longitude"
          id="longitude"
          type="text"
          :class="getInputClass('longitude')"
          @blur="v$.longitude.$touch"
        />
        <label for="longitude" class="placeholder">
          <span>Longitude</span>
        </label>
        <ul v-if="v$.longitude.$error">
          <li v-for="(error, index) in v$.longitude.$errors" :key="index">
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
import {
  helpers,
  required,
  alpha,
  alphaNum,
  sameAs,
  numeric,
  minLength,
  maxLength,
  between,
} from "@vuelidate/validators";
import { computed, reactive } from "vue";

const state = reactive({
  account: "",
  password: "",
  confirm: "",
  name: "",
  phone: "",
  latitude: null,
  longitude: null,
});

const accountValidation = helpers.withAsync(async (value: string) => {
  if (value.length === 0) return true;
  try {
    await axios.get(`/getuser/${value}`);
  } catch (error) {
    return true;
  }
  return false;
});

const rules = {
  account: {
    required,
    alphaNum,
    checkAccount: helpers.withMessage(
      "Account already been registered",
      accountValidation
    ),
  },
  password: { required, alphaNum },
  confirm: {
    required,
    alphaNum,
    sameAs: helpers.withMessage(
      "Check your password again",
      sameAs(computed(() => state.password))
    ),
  },
  name: { required, alpha },
  phone: {
    required,
    digits: helpers.withMessage("Invalid phone number", helpers.regex(/^09\d{8}$/))
  },
  latitude: { required, numeric, between: between(-90, 90) },
  longitude: { required, numeric, between: between(-180, 180) },
};

const v$ = useVuelidate(rules, state);

function getInputClass<Key extends keyof typeof state>(field: Key) {
  return (
    (v$.value[field].$error ? "danger" : "") + (state[field] ? " filled" : "")
  );
}

async function handleSubmit() {
  const isFormCorrect = await v$.value.$validate();
  if (!isFormCorrect) return;

  try {
    const response = await axios.post("/register", {
      account: state.account,
      password: state.password,
      phone: state.phone,
      realname: state.name,
      latitude: state.latitude,
      longitude: state.longitude,
    });
    console.log(response.data);
  } catch (error) {
    alert("Registration failed");
    return;
  }
}
</script>

<style scoped lang="scss"></style>
