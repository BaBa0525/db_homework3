<template>
  <div class="input">
    <input v-bind="$attrs" type="file" :class="{ 'filled': isFilled, 'danger': hasError }" ref="fileInput"
      @input="onFileSelect" />
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
import { ref, toRefs, watch, computed } from 'vue';

const props = defineProps(['placeholder', 'hasError', 'errors', 'fileModel']);
const emit = defineEmits(['fileChange']);

const { fileModel } = toRefs(props);
const fileInput = ref(null);

const isFilled = computed(() => (!!fileModel.value));

const onFileSelect = () => {
  const input = fileInput.value;
  const files = input.files;

  if (files && files[0]) {
    const reader = new FileReader();

    reader.onloadend = () => {
      emit('fileChange', reader.result);
    };

    reader.readAsDataURL(files[0]);
  }
  else {
    emit('fileChange', null);
  }
}

watch(fileModel, (value) => {
  if (value === null) {
    fileInput.value.value = '';
  }
})
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

    &[type="file"] {
      cursor: pointer;

      &::-webkit-file-upload-button {
        display: none;
      }
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
