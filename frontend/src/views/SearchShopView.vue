<template>
  <div class="form-container"
    :style="{ 'margin': '0 auto', 'max-width': `calc(100% - ${sidebar.sidebarWidth} - 4rem)` }">
    <BaseRowForm @submit.prevent="handleSubmit" button-text="Search"
      :disableButton="v$.$error || v$.$errors.length > 0">
      <BaseInput v-model="state.shopname" placeholder="Shop Name" :hasError="v$.shopname.$error"
        :errors="v$.shopname.$errors" id="shopname" type="text" :styling="{ width: `calc(100% / 7)` }"
        @blur="v$.shopname.$touch" />
      <BaseDropDown v-model="state.distance" placeholder="Distance" :hasError="v$.distance.$error"
        :errors="v$.distance.$errors" id="distance" :options="options" :styling="{ width: `calc(100% / 7)` }"
        @blur="v$.distance.$touch" />
      <BaseInput v-model="state.pricelow" placeholder="Price Low" :hasError="v$.pricelow.$error"
        :errors="v$.pricelow.$errors" id="pricelow" type="text" :styling="{ width: `calc(100% / 7)` }"
        @blur="v$.pricelow.$touch" />
      <BaseInput v-model="state.pricehigh" placeholder="Price High" :hasError="v$.pricehigh.$error"
        :errors="v$.pricehigh.$errors" id="pricehigh" type="text" :styling="{ width: `calc(100% / 7)` }"
        @blur="v$.pricehigh.$touch" />
      <BaseInput v-model="state.category" placeholder="Category" :hasError="v$.category.$error"
        :errors="v$.category.$errors" id="category" type="text" :styling="{ width: `calc(100% / 7)` }"
        @blur="v$.category.$touch" />
      <BaseInput v-model="state.meal" placeholder="Meal" :hasError="v$.meal.$error" :errors="v$.meal.$errors" id="meal"
        type="text" :styling="{ width: `calc(100% / 7)` }" @blur="v$.meal.$touch" />
    </BaseRowForm>
  </div>

  <div class="table-container"
    :style="{ 'margin': '0 auto', 'max-width': `calc(100% - ${sidebar.sidebarWidth} - 4rem)` }">
    <BaseTable :fields="shopsField" :items="shops" @sort-by="handleSorting">
      <template #cell(distance)="{ item }">
        {{ Math.round(item.distance) }} m
      </template>
      <template #cell(action)="{ item }">
        <button type="button" @click="handleTogglePopup(item)">Open Menu</button>
      </template>
    </BaseTable>
  </div>

  <ul class="page-list">
    <li v-for="pageNumber in totalPages" :class="{ 'current-page': (state.page === pageNumber) }"
      @click="handleChangePage(pageNumber)">{{ pageNumber }}</li>
  </ul>

  <!-- menu -->
  <PopupModal :show="popupShop.active" :titles="`Menu of ${popupShop.shopname}`"
    @close-popup="popupShop.active = false">
    <BaseTable :fields="mealsField" :items="meals">
      <template #cell(picture)="{ item }">
        <BaseImage :src="item.image" :alt="item.name" width="100" height="100"></BaseImage>
      </template>
      <template #cell(order)="{ item }">
        <button type="button" :disabled="item.orderQuantity <= 0" @click="editQuantity(item, -1)">-</button>
        <span>{{ item.orderQuantity }}</span>
        <button type="button" :disabled="item.orderQuantity >= item.quantity" @click="editQuantity(item, 1)">+</button>
      </template>
    </BaseTable>
    <BaseDropDown v-model="type" :options="typeOption"></BaseDropDown>
    <button type="button" :disabled="isOrderEmpty" @click="handleCalculatePrice()">Calculate Price</button>
  </PopupModal>

  <!-- order -->
  <PopupModal :show="popupOrder.active" titles="Order Preview" @close-popup="popupOrder.active = false">
    <BaseTable :fields="orderField" :items="orderMeals">
      <template #cell(picture)="{ item }">
        <BaseImage :src="item.image" :alt="item.name" width="100" height="100"></BaseImage>
      </template>
    </BaseTable>
    <div class="totalprice">
      <p>Subtotal ${{ subtotal }}</p>
      <p>Delivery Fee ${{ deliverFee }}</p>
      <hr>
      <p>Total Price ${{ subtotal + deliverFee }}</p>
    </div>
    <button type="button" :disable="userStore.balance < (subtotal + deliverFee)" @click="handleOrder">Order</button>
  </PopupModal>
</template>

<script setup>
import { ref, reactive, computed } from "vue";
import useVuelidate from "@vuelidate/core";
import { decimal, alphaNum, minValue, helpers } from "@vuelidate/validators";
import { useUserStore } from "@/stores/user";
import { useSidebarStore } from "../stores/sidebar";
import axios from "axios";
import haversine from "haversine";
import BaseInput from "../components/BaseInput.vue";
import BaseImage from "../components/BaseImage.vue";
import BaseDropDown from "../components/BaseDropDown.vue";
import BaseRowForm from "../components/BaseRowForm.vue";
import BaseTable from "../components/BaseTable.vue";
import PopupModal from "../components/PopupModal.vue";

const options = ['near', 'middle', 'far'];
const sidebar = useSidebarStore();

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

const shopsField = [
  { key: 'index', sortable: false },
  { key: 'shopname', sortable: true },
  { key: 'distance', sortable: true },
  { key: 'category', sortable: true },
  { key: 'action', sortable: false },
];

const shops = reactive([]);

const updateShopList = async (orderString = '') => {
  try {
    const response = await axios.post('/getshop', {
      ...state,
      latitude: userStore.latitude,
      longitude: userStore.longitude,
      order: orderString,
    });

    const shopsResponse = response.data.shops;
    const countResponse = response.data.count;

    totalPages.value = Math.ceil(countResponse / 5);
    let indexCounter = 1;

    shops.splice(0, shops.length);

    for (const shop of shopsResponse) {
      shops.push({
        index: indexCounter++,
        shopname: shop.shopname,
        distance: haversine(
          { latitude: userStore.latitude, longitude: userStore.longitude },
          { latitude: shop.latitude, longitude: shop.longitude },
          { unit: 'meter' }),
        category: shop.category,
      });
    }
  } catch (error) {
    console.log(error);
  }
}

const handleSubmit = async () => {
  v$.value.$touch();
  if (v$.value.$error) return;
  await updateShopList();
}

const handleSorting = async (key, order) => {
  if (shops.length === 0) return;
  await updateShopList(`${key}$${order}`);
}

const handleChangePage = async (pageNumber) => {
  if (state.page === pageNumber) return;
  alert('change to page ' + pageNumber);
  state.page = pageNumber;
  await updateShopList();
}

const popupShop = reactive({
  active: false,
  shopname: '',
});

const meals = reactive([]);

const getMeals = async () => {
  meals.splice(0, meals.length);
  try {
    const response = await axios.get(`/getmeal/${popupShop.shopname}`);
    const mealsResponse = response.data;
    let indexCounter = 1;

    for (const meal of mealsResponse) {
      meals.push({
        ...meal,
        index: indexCounter++,
        orderQuantity: 0,
      });
    }

  } catch (error) {
    console.log(error);
  }
};

const handleTogglePopup = async (item) => {
  popupShop.active = true;
  popupShop.shopname = item.shopname;
  await getMeals();
}

// shop popup
const mealsField = [
  { key: 'index', sortable: false },
  { key: 'picture', sortable: false },
  { key: 'name', sortable: false },
  { key: 'price', sortable: false },
  { key: 'quantity', sortable: false },
  { key: 'order', sortable: false },
];

const typeOption = ['Delivery', 'Pickup'];

const type = ref('Delivery');

const editQuantity = (item, quantity) => {
  item.orderQuantity += quantity;
}

const handleCalculatePrice = () => {
  orderMeals.value = meals.filter((item) => (item.orderQuantity > 0));
  popupShop.active = false;
  popupOrder.active = true;
}

// order popup
const orderMeals = ref([]);

const popupOrder = reactive({
  active: false,
});

const subtotal = computed(() => {
  let subtotal = 0;
  for (const meal of orderMeals.value) {
    subtotal += meal.price * meal.orderQuantity;
  }
  return subtotal;
});

const deliverFee = computed(() => {
  const dist = shops.filter((item) => (item.shopname === popupShop.shopname))[0].distance;
  if (type.value === 'Pickup') {
    return 0;
  }
  else {
    return Math.round(Math.max(10, (dist / 1000) * 10));
  }
});

const handleOrder = async () => {
  try {
    await axios.post('/addorder', {
      account: userStore.account,
      shopname: popupShop.shopname,
      meals: orderMeals.value,
      type: type.value,
      subtotal: subtotal.value,
      deliverFee: deliverFee.value,
    });
    alert("Order Successfully");
  } catch (error) {
    alert(error.response.data.message);
  }

  popupOrder.active = false;
};

const orderField = [
  { key: 'picture', sortable: false },
  { key: 'name', sortable: false },
  { key: 'price', sortable: false },
  { key: 'orderQuantity', sortable: false },
];

const isOrderEmpty = computed(() => {
  let isEmpty = true;
  for (const meal of meals) {
    if (meal.orderQuantity > 0) {
      isEmpty = false;
      break;
    }
  }
  return isEmpty;
});

</script>


<style scoped lang="scss">
@import "@/styles/global.scss";

.form-container {
  position: absolute;
  top: 5%;
}

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

.page-list {
  @include flex-row;
  gap: 25px;

  li {
    list-style: none;
    font-size: 1.05rem;
    cursor: pointer;
    color: var(--text-color);
    font-weight: 300;

    &.current-page {
      color: var(--info-color);
      font-weight: 600;
    }
  }
}
</style>