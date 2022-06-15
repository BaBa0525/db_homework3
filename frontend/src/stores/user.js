import axios from 'axios';
import { defineStore } from 'pinia';

export const useUserStore = defineStore({
    id: 'user',
    persist: true,
    state: () => ({
        realname: '',
        role: '',
        account: '',
        phone: '',
        password: '',
        latitude: null,
        longitude: null,
        balance: 0,
        shopname: '',
    }),
    getters: {
        isLogin: (state) => (state.account && state.account.length > 0),
        isOwner: (state) => (state.role === 'owner'),
    },
    actions: {
        logout() {
            this.$reset();
        },
        async reload() {
            if (this.account === '') return;
            const response = await axios.get(`/getuser/${this.account}`);
            for (const property in this.$state) {
                this[property] = response.data[property];
            }
        },
    }
});
