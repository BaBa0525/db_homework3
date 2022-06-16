<template>
  <div class="input" :style="styling">
    <input v-bind="$attrs" :value="modelValue" :class="{ 'filled': modelValue, 'danger': hasError }"
      @input="$emit('update:modelValue', $event.target.value)" />
    <label class="placeholder">
      <span>{{ placeholder }}</span>
    </label>
    <ul v-if="hasError">
      <li v-for="(error, index) in errors" :key="index">
        {{ error.$message }}
      </li>
    </ul>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: '',
  },
  placeholder: {
    type: String,
    default: '',
  },
  hasError: {
    type: Boolean,
    default: false,
  },
  errors: {
    type: Array,
    default: () => [],
  },
  styling: {
    type: Object,
    default: () => ({}),
  }
});
</script>

<style scoped lang="scss">
@import "@/styles/global.scss";

.input {
  position: relative;
  @include flex;

  input {
    border: 2px solid var(--secondary-color);
    border-radius: 8px;
    background-color: var(--secondary-color);
    outline: none;
    color: var(--text-color);
    padding: 10px 12px;
    box-sizing: border-box;
    font-size: 14px;
    transition: all 0.3s ease;

    &:focus,
    &:hover,
    &.filled {
      border: 2px solid var(--info-color);
    }

    &:focus+.placeholder span,
    &.filled+.placeholder span {
      transform: translateY(-100%);
    }

    &.danger {
      border: 2px solid var(--danger-color);
    }

    &:disabled {
      cursor: not-allowed;
      border: 2px solid var(--secondary-color);
    }
  }

  .placeholder {
    @include flex;
    position: absolute;
    width: calc(100% - 24px);
    top: 10px;
    left: 12px;
    pointer-events: none;
    overflow: hidden;

    span {
      transition: all 0.3s ease;
      font-size: 14px;
    }
  }

  ul {
    color: var(--danger-color);
    list-style-type: none;
    padding: 0;
    margin: 5px;
    font-size: 12px;
    gap: 4px;
  }
}
</style>
