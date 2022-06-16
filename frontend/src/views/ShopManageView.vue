<template>
  <div class="container">
    <BaseRowForm @submit.prevent="handleRegister" buttonText="Register"
      :disableButton="userStore.isOwner || shopv$.$error || shopv$.$errors.length > 0">
      <BaseInput :disabled="userStore.isOwner" v-model="shopState.shopname" placeholder="Shop Name"
        :hasError="shopv$.shopname.$error" :errors="shopv$.shopname.$errors" id="shopname" type="text"
        @blur="shopv$.shopname.$touch" />
      <BaseInput :disabled="userStore.isOwner" v-model="shopState.category" placeholder="Category"
        :hasError="shopv$.category.$error" :errors="shopv$.category.$errors" id="category" type="text"
        @blur="shopv$.category.$touch" />
      <BaseInput :disabled="userStore.isOwner" v-model="shopState.latitude" placeholder="Latitude"
        :hasError="shopv$.latitude.$error" :errors="shopv$.latitude.$errors" id="latitude" type="text"
        @blur="shopv$.latitude.$touch" />
      <BaseInput :disabled="userStore.isOwner" v-model="shopState.longitude" placeholder="Longitude"
        :hasError="shopv$.longitude.$error" :errors="shopv$.longitude.$errors" id="longitude" type="text"
        @blur="shopv$.longitude.$touch" />
    </BaseRowForm>

    <BaseRowForm @submit.prevent="handleAddMeal" buttonText="Add"
      :disableButton="!userStore.isOwner || mealv$.$error || mealv$.$errors.length > 0">
      <BaseInput :disabled="!userStore.isOwner" v-model="mealState.mealname" placeholder="Meal Name"
        :hasError="mealv$.mealname.$error" :errors="mealv$.mealname.$errors" id="mealname" type="text"
        @blur="mealv$.mealname.$touch" />
      <BaseInput :disabled="!userStore.isOwner" v-model="mealState.price" placeholder="Price"
        :hasError="mealv$.price.$error" :errors="mealv$.price.$errors" id="price" type="text"
        @blur="mealv$.price.$touch" />
      <BaseInput :disabled="!userStore.isOwner" v-model="mealState.quantity" placeholder="Quantity"
        :hasError="mealv$.quantity.$error" :errors="mealv$.quantity.$errors" id="quantity" type="text"
        @blur="mealv$.quantity.$touch" />
      <FileInput :disabled="!userStore.isOwner" :hasError="mealv$.image.$error" :errors="mealv$.image.$errors"
        id="image" accept="image/*" :fileModel="mealState.image" @fileChange="handleFileChange" />
    </BaseRowForm>

    <BaseTable :fields="fields" :items="meals">
      <template #cell(photo)="{ item }">
        <BaseImage :src="item.image" :alt="item.name" width="100" height="100"></BaseImage>
      </template>
      <template #cell(price)="{ item }">
        <BaseInput :disabled="!item.isEditing" v-model="item.price" :hasError="item.v$.price.$error"
          :errors="item.v$.price.$errors" type="text" @blur="item.v$.price.$touch"
          style="text-align: center; cursor: default;" />
      </template>
      <template #cell(quantity)="{ item }">
        <BaseInput :disabled="!item.isEditing" v-model="item.quantity" :hasError="item.v$.quantity.$error"
          :errors="item.v$.quantity.$errors" type="text" @blur="item.v$.quantity.$touch"
          style="text-align: center; cursor: default;" />
      </template>
      <template #cell(edit)="{ item }">
        <button type="button" :disabled="item.v$.$error || item.v$.$errors.length > 0" @click="handleEdit(item)">
          <span v-if="item.isEditing">Finish</span>
          <span v-else>Edit</span>
        </button>
      </template>
      <template #cell(delete)="{ item }">
        <button type="button" @click="handleDelete(item)">Delete</button>
      </template>
    </BaseTable>
  </div>
</template>

<script setup>
import BaseRowForm from '../components/BaseRowForm.vue';
import BaseInput from '../components/BaseInput.vue';
import FileInput from '../components/FileInput.vue';
import BaseTable from '../components/BaseTable.vue';
import BaseImage from '../components/BaseImage.vue';
import { useUserStore } from '../stores/user';

import axios from 'axios';
import { ref, reactive, computed } from 'vue';
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

const loadUserShop = async () => {
  try {
    const response = await axios.get(`/getshop/${userStore.shopname}`);
    for (const property in shopState) {
      shopState[property] = response.data[property];
    }
  } catch (error) {
    console.log(error);
  }
};

const editRules = computed(() => ({
  price: { required, decimal, minValue: minValue(0), },
  quantity: { required, decimal, minValue: minValue(0), },
}));

const loadShopMeals = async () => {
  try {
    const response = await axios.get(`/getmeal/${userStore.shopname}`);
    const mealsResponse = response.data;

    let indexCounter = 1;
    meals.splice(0, meals.length);

    for (const meal of mealsResponse) {
      meals.push({
        index: indexCounter++,
        isEditing: false,
        ...meal,
      });

      meals[meals.length - 1].v$ = useVuelidate(editRules, meals[meals.length - 1]);
    }
  } catch (error) {
    console.log(error);
  }
}

const startup = async () => {
  if (!userStore.isOwner) return;

  await loadUserShop();
  await loadShopMeals();
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
  category: { required, },
  latitude: { required, decimal, between: between(-90, 90), },
  longitude: { required, decimal, between: between(-180, 180), },
}));

const shopv$ = useVuelidate(shopRules, shopState);

const handleRegister = async () => {
  shopv$.value.$touch();

  if (shopv$.value.$error || shopv$.value.$errors.length > 0) return;

  try {
    await axios.post('/addshop', {
      ...shopState,
      account: userStore.account,
    });
    alert('Registration succeed!');
    await userStore.reload();
    await loadUserShop();
  } catch (error) {
    console.log(error);
  }
}

const mealState = reactive({
  mealname: '',
  price: '',
  quantity: '',
  shopname: '',
  image: null,
});

const mealRules = computed(() => ({
  mealname: { required, },
  price: { required, decimal, minValue: minValue(0), },
  quantity: { required, decimal, minValue: minValue(0), },
  image: { required, },
}));

const mealv$ = useVuelidate(mealRules, mealState);

const handleFileChange = (file) => {
  mealState.image = file;
  mealv$.value.image.$touch();
}

const handleAddMeal = async () => {
  mealv$.value.$touch();
  if (mealv$.value.$error || mealv$.value.$errors.length > 0) return;
  try {
    await axios.post('/addmeal', {
      ...mealState,
      shopname: shopState.shopname,
    });
    await loadShopMeals();
  } catch (error) {
    alert('Something went wrong, please check your meal details again.');
  }
  mealState.mealname = '';
  mealState.price = '';
  mealState.quantity = '';
  mealState.shopname = '';
  mealState.image = null;
  mealv$.value.$reset();
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
  try {
    if (item.isEditing) {
      item.v$.$touch();
      if (item.v$.$error || item.v$.$errors.length > 0) return;

      await axios.patch('/editmeal', {
        shopname: item.shopname,
        mealname: item.name,
        price: item.price,
        quantity: item.quantity,
      });
    }

    item.isEditing = !item.isEditing;

  } catch (error) {
    console.log(error);
  }
}

const handleDelete = async (item) => {
  await axios.post('/deletemeal', {
    shopname: item.shopname,
    mealname: item.name,
  });
  await loadShopMeals();
}
</script>

<style scoped lang="scss">
@import "@/styles/global.scss";

.container {
  @include flex;
  align-items: flex-start;
  gap: 3rem;

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
}
</style>