<template>
  <BaseRowForm @submit.prevent="handleSubmit" button-text="Search" :disableButton="v$.$error || v$.$errors.length > 0">
    <BaseInput v-model="state.shopname" placeholder="Shop Name" :hasError="v$.shopname.$error"
      :errors="v$.shopname.$errors" id="shopname" type="text" @blur="v$.shopname.$touch" />
    <BaseDropDown v-model="state.distance" placeholder="Distance" :hasError="v$.distance.$error"
      :errors="v$.distance.$errors" id="distance" :options="options" @blur="v$.distance.$touch" />
    <BaseInput v-model="state.pricelow" placeholder="Price Low" :hasError="v$.pricelow.$error"
      :errors="v$.pricelow.$errors" id="pricelow" type="text" @blur="v$.pricelow.$touch" />
    <BaseInput v-model="state.pricehigh" placeholder="Price High" :hasError="v$.pricehigh.$error"
      :errors="v$.pricehigh.$errors" id="pricehigh" type="text" @blur="v$.pricehigh.$touch" />
    <BaseInput v-model="state.category" placeholder="Category" :hasError="v$.category.$error"
      :errors="v$.category.$errors" id="category" type="text" @blur="v$.category.$touch" />
    <BaseInput v-model="state.meal" placeholder="Meal" :hasError="v$.meal.$error" :errors="v$.meal.$errors" id="meal"
      type="text" @blur="v$.meal.$touch" />
  </BaseRowForm>

  <div class="table-container">
    <BaseTable :fields="shopsField" :items="shops" @sort-by="handleSorting">
      <template #cell(action)="{ item }">
        <button type="button" @click="handleTogglePopup(item)">Open Menu</button>
      </template>
    </BaseTable>
  </div>

  <ul>
    <li v-for="pageNumber in totalPages">{{ pageNumber }}</li>
  </ul>

  <PopupModal :show="popupShop.active" @close-popup="popupShop.active = false">
    <h1>Menu of {{ popupShop.shopname }}</h1>
    <BaseTable :fields="mealsField" :items="meals">
      <template #cell(order)="{ item }">
        <button type="button" @click="addToOrder(item)">Order</button>
      </template>
    </BaseTable>
  </PopupModal>
</template>

<script setup>
import { ref, reactive, computed } from "vue";
import useVuelidate from "@vuelidate/core";
import { decimal, alphaNum, minValue, helpers } from "@vuelidate/validators";
import { useUserStore } from "@/stores/user";
import axios from "axios";
import haversine from "haversine";
import BaseInput from "../components/BaseInput.vue";
import BaseDropDown from "../components/BaseDropDown.vue";
import BaseRowForm from "../components/BaseRowForm.vue";
import BaseTable from "../components/BaseTable.vue";
import PopupModal from "../components/PopupModal.vue";

const options = ['near', 'middle', 'far'];

const state = reactive({
  shopname: '',
  distance: '',
  pricelow: '',
  pricehigh: '',
  category: '',
  meal: '',
  page: 1,
});

const rules = computed(() => ({
  shopname: {
    alphaNum,
  },
  distance: {},
  pricelow: {
    decimal,
    minValue: helpers.withMessage('Invalid minimum price', minValue(0)),
  },
  pricehigh: {
    decimal,
    minValue: helpers.withMessage('Invalid maximum price', minValue(Math.max(0, state.pricelow))),
  },
  category: {},
  meal: {},
}));

const v$ = useVuelidate(rules, state);

const userStore = useUserStore();
const totalPages = ref(0);

const parseResponse = (response) => {
  const shopsResponse = response.data.shops;
  const countResponse = response.data.count;

  totalPages.value = Math.ceil(countResponse / 5);
  let indexCounter = 1;

  for (const shop in shopsResponse) {
    shops.push({
      index: indexCounter++,
      shop_name: shop.shopname,
      distance: haversine(
        [userStore.latitude, userStore.longitude],
        [shop.latitude, shop.longitude],
        { unit: 'meter', format: '[lat, lon]' }),
      category: shop.category,
    });
  }
}

const shopsField = [
  { key: 'index', sortable: false },
  { key: 'shopname', sortable: true },
  { key: 'distance', sortable: true },
  { key: 'category', sortable: true },
  { key: 'action', sortable: false },
];

const shops = reactive([
  { index: 1, shopname: 'shop1', distance: 345, category: 'category1', action: 'action1' },
  { index: 2, shopname: 'shop2', distance: 3520, category: 'category2', action: 'action2' },
  { index: 3, shopname: 'shop3', distance: 1234, category: 'category3', action: 'action3' },
]);

const handleSubmit = async () => {
  v$.value.$touch();

  if (v$.value.$error) {
    return;
  }

  try {
    const response = await axios.post('/getshop', {
      ...state,
      latitude: userStore.latitude,
      longitude: userStore.longitude,
      order: '',
    });

    parseResponse(response);

  } catch (error) {
    console.log(error);
  }
}

const handleSorting = async (key, order) => {
  try {
    const response = await axios.post('/getshop', {
      ...state,
      latitude: userStore.latitude,
      longitude: userStore.longitude,
      order: `${key}$${order}`,
    });

    parseResponse(response);

  } catch (error) {
    console.log(error);
  }
}

const popupShop = reactive({
  active: false,
});

const meals = reactive([]);

const getMeals = async () => {
  meals.splice(0, meals.length);
  try {
    const response = await axios.get(`/getmeal/${popupShop.shopname}`);
    let indexCounter = 1;

    for (const meal in response.data) {
      meals.push({
        ...meal,
        index: indexCounter++,
      });
    }

  } catch (error) {
    console.log(error);
  }
};

const handleTogglePopup = (item) => {
  popupShop.active = true;
  popupShop.shopname = item.shopname;
  getMeals();
}

const mealsField = [
  { key: 'index', sortable: false },
  { key: 'picture', sortable: false },
  { key: 'name', sortable: false },
  { key: 'price', sortable: false },
  { key: 'quantity', sortable: false },
  { key: 'order', sortable: false },
];

const addToOrder = async () => {
  alert('TODO: add to order');
};
</script>

<style scoped lang="scss">
button {
  border: none;
  border-radius: 4px;
  padding: 10px 12px;
  background-color: var(--info-color);
  color: var(--white-color);
  cursor: pointer;
  transition: all 0.3s ease;

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}
</style>