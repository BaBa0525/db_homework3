import { defineStore } from 'pinia';

export const useUserStore = defineStore({
    id: 'user',
    persist: true,
    state: () => ({
        account: '',
        password: '',
        realname: '',
        phone: '',
        latitude: null,
        longitude: null,
    }),
    getters: {
        isLogin: (state) => (state.account && state.account.length > 0),
    },
    actions: {
        logout() {
            this.$reset();
        },
    }
});
