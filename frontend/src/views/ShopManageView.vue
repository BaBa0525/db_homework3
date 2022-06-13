<template>
  <BaseRowForm @submit.prevent="handleRegister" buttonText="Register"
    :disableButton="isUserHasShop || shopv$.$error || shopv$.$errors.length > 0">
    <BaseInput :disabled="isUserHasShop" v-model="shopState.shopname" placeholder="Shop Name"
      :hasError="shopv$.shopname.$error" :errors="shopv$.shopname.$errors" id="shopname" type="text"
      @blur="shopv$.shopname.$touch" />
    <BaseInput :disabled="isUserHasShop" v-model="shopState.category" placeholder="Category"
      :hasError="shopv$.category.$error" :errors="shopv$.category.$errors" id="category" type="text"
      @blur="shopv$.category.$touch" />
    <BaseInput :disabled="isUserHasShop" v-model="shopState.latitude" placeholder="Latitude"
      :hasError="shopv$.latitude.$error" :errors="shopv$.latitude.$errors" id="latitude" type="text"
      @blur="shopv$.latitude.$touch" />
    <BaseInput :disabled="isUserHasShop" v-model="shopState.longitude" placeholder="Longitude"
      :hasError="shopv$.longitude.$error" :errors="shopv$.longitude.$errors" id="longitude" type="text"
      @blur="shopv$.longitude.$touch" />
  </BaseRowForm>

  <BaseRowForm @submit.prevent="handleAddMeal" buttonText="Add"
    :disableButton="!isUserHasShop || mealv$.$error || mealv$.$errors.length > 0">
    <BaseInput :disabled="!isUserHasShop" v-model="mealState.mealname" placeholder="Meal Name"
      :hasError="mealv$.mealname.$error" :errors="mealv$.mealname.$errors" id="mealname" type="text"
      @blur="mealv$.mealname.$touch" />
    <BaseInput :disabled="!isUserHasShop" v-model="mealState.price" placeholder="Price" :hasError="mealv$.price.$error"
      :errors="mealv$.price.$errors" id="price" type="text" @blur="mealv$.price.$touch" />
    <BaseInput :disabled="!isUserHasShop" v-model="mealState.quantity" placeholder="Quantity"
      :hasError="mealv$.quantity.$error" :errors="mealv$.quantity.$errors" id="quantity" type="text"
      @blur="mealv$.quantity.$touch" />
    <FileInput :disabled="!isUserHasShop" :hasError="mealv$.image.$error" :errors="mealv$.image.$errors" id="image"
      accept="image/*" @change="handleImageChange" />
  </BaseRowForm>

  <BaseTable :fields="fields" :items="meals">
    <template #cell(photo)="{ item }">
      <BaseImage :src="item.image" :alt="item.name" width="100" height="100"></BaseImage>
    </template>
    <template #cell(price)="{ item }">
      <BaseInput :disabled="!item.isEditing" v-model="item.price" placeholder="Quantity" type="text"
        style="text-align: center; cursor: default;" />
    </template>
    <template #cell(quantity)="{ item }">
      <BaseInput :disabled="!item.isEditing" v-model="item.quantity" placeholder="Quantity" type="text"
        style="text-align: center; cursor: default;" />
    </template>
    <template #cell(edit)="{ item }">
      <button type="button" @click="handleEdit(item)">
        <span v-if="item.isEditing">Finish</span>
        <span v-else>Edit</span>
      </button>
    </template>
    <template #cell(delete)="{ item }">
      <button type="button" @click="handleDelete(item)">Delete</button>
    </template>
  </BaseTable>
</template>

<script setup>
import BaseRowForm from '../components/BaseRowForm.vue';
import BaseInput from '../components/BaseInput.vue';
import FileInput from '../components/FileInput.vue';
import BaseTable from '../components/BaseTable.vue';
import BaseImage from '../components/BaseImage.vue';
import { useUserStore } from '../stores/user';

import axios from 'axios';
import { useRouter } from 'vue-router';
import { reactive, computed, ref } from 'vue';
import useVuelidate from '@vuelidate/core';
import { required, decimal, between, helpers, minValue } from '@vuelidate/validators';

const userStore = useUserStore();

const shopState = reactive({
  shopname: '',
  category: '',
  latitude: '',
  longitude: '',
});
const meals = reactive([]);

const startup = async () => {
  try {
    const response = await axios.get(`/getshop/${userStore.account}`);
    shopState.shopname = response.data.shopname;
    shopState.category = response.data.category;
    shopState.latitude = response.data.latitude;
    shopState.longitude = response.data.longitude;
  } catch (error) {
    console.log(error);
  }

  try {
    const response = await axios.get(`/getmeal/${shopState.shopname}`);
    const mealsResponse = response.data;
    let indexCounter = 1;
    for (const i in mealsResponse) {
      const meal = mealsResponse[i];
      meals.push({
        index: indexCounter++,
        ...meal,
      });
    }
  } catch (error) {
    console.log(error);
  }
};

startup();

const isShopnameUnique = async () => {
  const response = await axios.get(`/checkshop/${shopState.shopname}`);
  return !response.data.exists;
}

const shopRules = computed(() => ({
  shopname: {
    required,
    unique: helpers.withMessage('The shop name has been registered', helpers.withAsync(isShopnameUnique)),
  },
  category: {
    required,
  },
  latitude: {
    required,
    decimal,
    between: between(-90, 90),
  },
  longitude: {
    required,
    decimal,
    between: between(-180, 180),
  },
}));

const shopv$ = useVuelidate(shopRules, shopState);
const router = useRouter();

const handleRegister = async () => {
  shopv$.value.$touch();

  if (shopv$.value.$error) return;

  try {
    await axios.post('/addshop', {
      ...shopState,
      account: userStore.account,
    });
    alert('Registration succeed!');
    router.go(0);
  } catch (error) {
    console.log(error);
  }
}

const isUserHasShop = computed(() => (shopState.shopname.length > 0));

const mealState = reactive({
  mealname: '',
  price: '',
  quantity: '',
  shopname: '',
  image: '',
});

const mealRules = computed(() => ({
  mealname: {
    required,
  },
  price: {
    required,
    decimal,
    minValue: minValue(0),
  },
  quantity: {
    required,
    decimal,
    minValue: minValue(0),
  },
  image: {
    required,
  },
}));

const mealv$ = useVuelidate(mealRules, mealState);

const handleImageChange = (event) => {
  const file = event.target.files[0];

  try {
    const reader = new FileReader();
    reader.onloadend = () => { mealState.image = reader.result };
    reader.readAsDataURL(file);
  } catch {
    mealState.image = '';
  }

  mealv$.value.image.$touch();
}

const handleAddMeal = async () => {
  mealv$.value.$touch();
  if (mealv$.value.$error) return;
  try {
    await axios.post('/addmeal', {
      ...mealState,
      shopname: shopState.shopname,
    });
    router.go(0);
  } catch (error) {
    console.log(error);
  }
}

const fields = [
  { key: 'index', sortable: false },
  { key: 'name', sortable: false },
  { key: 'photo', sortable: false },
  { key: 'price', sortable: false },
  { key: 'quantity', sortable: false },
  { key: 'edit', sortable: false },
  { key: 'delete', sortable: false },
];

const handleEdit = async (item) => {
  item.isEditing = !item.isEditing;
  if (item.isEditing) {

  } else {

  }
}

const handleDelete = async (item) => {

}
</script>

<style scoped lang="scss">
@import "@/styles/global.scss";

button {
  border: none;
  border-radius: 4px;
  padding: 10px 12px;
  background-color: var(--info-color);
  color: var(--white-color);
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100px;

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}
</style>