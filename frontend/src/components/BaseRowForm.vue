<template>
    <form>
        <slot></slot>
        <button type="submit" :disabled="disableButton">{{ buttonText }}</button>
    </form>
</template>

<script setup>
const props = defineProps({
    buttonText: {
        type: String,
        default: 'Submit',
    },
    disableButton: {
        type: Boolean,
        default: false,
    },
});
</script>

<style scoped lang="scss">
@import "@/styles/global.scss";

form {
    @include flex-row;
    gap: 20px;
    width: auto;
    padding: 20px;
    box-sizing: border-box;
    box-shadow: 0px 14px 20px 12px #00000012;
    border-radius: 8px;
    color: var(--text-color);
    align-items: flex-start;

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
}
</style>