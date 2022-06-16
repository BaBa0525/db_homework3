import { defineStore } from 'pinia'

export const useSidebarStore = defineStore({
  id: 'sidebar',
  state: () => ({
    collapsed: false
  }),
  getters: {
    SIDEBAR_WIDTH: (state) => (200),
    SIDEBAR_WIDTH_COLLAPSED: (state) => (38),
    sidebarWidth: (state) => (`${state.collapsed ? state.SIDEBAR_WIDTH_COLLAPSED : state.SIDEBAR_WIDTH}px`),
  },
  actions: {
    toggle() {
      this.collapsed = !this.collapsed;
    }
  }
})
