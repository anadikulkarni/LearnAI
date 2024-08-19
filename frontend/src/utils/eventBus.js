import { ref } from 'vue';

export const EventBus = {
  events: ref({}),
  
  $on(event, callback) {
    if (!this.events.value[event]) {
      this.events.value[event] = [];
    }
    this.events.value[event].push(callback);
  },

  $emit(event, ...args) {
    if (this.events.value[event]) {
      this.events.value[event].forEach(callback => callback(...args));
    }
  },
};