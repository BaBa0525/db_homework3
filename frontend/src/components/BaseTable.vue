<template>
  <table>
    <thead>
      <tr>
        <th v-for="(field, index) in fields" :key="index" :class="{ 'clickable': field.sortable }"
          @click="handleClick(field)">
          {{ getTitle(field.key) }}
          <IconSortable v-if="field.sortable" :status="status[field.key]"></IconSortable>
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(item, index) in items" :key="index">
        <td v-for="field in fields">
          <slot :name="`cell(${field.key})`" :item="item">
            {{ item[field.key] }}
          </slot>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
import { reactive } from 'vue';
import IconSortable from './icons/IconSortable.vue';

const props = defineProps({
  fields: {
    type: Array,
    default: () => [],
  },
  items: {
    type: Array,
    default: () => [],
  },
});

const getTitle = (str) => {
  const array = str.split('_');
  const result = array.map((word) => (word.charAt(0).toUpperCase() + word.slice(1)));
  return result.join(' ');
}

const status = reactive({});

const resetStatus = () => {
  for (const field in props.fields) {
    if (props.fields[field].sortable) {
      status[props.fields[field].key] = 'none';
    }
  }
}

resetStatus();

const emit = defineEmits(['sort-by']);

const handleClick = (field) => {
  if (!field.sortable) return;

  const key = field.key;
  const originalStatus = status[key];

  resetStatus();

  if (originalStatus === 'asc') {
    status[key] = 'desc';
  } else {
    status[key] = 'asc';
  }
  emit('sort-by', key, status[key]);
}
</script>

<style scoped lang="scss">
@import "@/styles/global.scss";

table {
  margin-top: 20px;
  margin-left: auto;
  margin-right: auto;
  border-radius: 4px;
  width: 75%;
  border-collapse: collapse;

  thead {
    tr {
      background: var(--gray-color);

      th {
        text-align: center;
        cursor: default;

        &.clickable {
          cursor: pointer;
        }
      }
    }
  }

  tbody {
    tr {
      background: var(--lightgray-color);

      td {
        text-align: center;

        button {
          background: var(--info-color);
          color: var(--white-color);
          border: none;
          padding: 20px 30px;
          border-radius: 5px;
          cursor: pointer;
        }
      }
    }

    input {
      width: 65px;
      text-align: center;
    }
  }
}
</style>