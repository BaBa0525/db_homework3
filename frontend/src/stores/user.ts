import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore("user", {
    state: () => ({
        user: {
            account: '',
            phone: '',
            password: '',
            realname: '',
            role: '',
            shopname: '',
            latitude: 0,
            longitude: 0,
            balance: 0n as bigint,
        }
    }),
    getters: {
        account: (state) => state.user.account,
    },
    actions: {
        setUser(user: any) {
            this.user = user;
        },
        addMoney(amount: bigint) {
            this.user.balance += amount;
        },
        async setPosition(latitude: number, longitude: number) {
            try {
                await axios.put("http://127.0.0.1/location", {
                    account: this.user.account,
                    latitude: latitude,
                    longitude: longitude,
                })
            }
            catch (error) {
                console.log(error);
                return;
            }

            // if no error
            this.user.latitude = latitude;
            this.user.longitude = longitude;
        }
    }
})