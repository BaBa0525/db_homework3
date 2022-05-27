import { defineStore } from "pinia";
import axios from "axios";
import type { User } from "@/types/typeUser";

function isEmptyUser(user: User) {
  for (const _ in user) {
    return false;
  }
  return true;
}

export const useUserStore = defineStore("user", {
  state: () => ({
    user: {} as User,
  }),
  getters: {
    isLoggedIn: (state) => !isEmptyUser(state.user),
    account: (state) => state.user.account,
  },
  actions: {
    setUser(user: User) {
      this.user = user;
    },
    addMoney(amount: number) {
      if (!this.user.balance) this.user.balance = amount;
      else this.user.balance += amount;
    },
    async setPosition(latitude: number, longitude: number) {
      try {
        await axios.put("/location", {
          account: this.user.account,
          latitude: latitude,
          longitude: longitude,
        });
      } catch (error) {
        console.log(error);
        return;
      }

      // if no error
      this.user.latitude = latitude;
      this.user.longitude = longitude;
    },
  },
});
