import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore("user", {
  state: () => ({
    user: {
      account: undefined,
      phone: undefined,
      password: undefined,
      realname: undefined,
      role: undefined,
      shopname: undefined,
      latitude: undefined,
      longitude: undefined,
      balance: undefined,
    } as User
  }),
  getters: {
    account: (state) => state.user.account,
  },
  actions: {
    setUser(user: User) {
      this.user = user;
    },
    addMoney(amount: number) {
      if (this.user.balance === undefined) this.user.balance = amount;
      else this.user.balance += amount;
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