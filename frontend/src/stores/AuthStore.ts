import { computed, ref } from "vue";
import { defineStore } from "pinia";
import type { Ref, ComputedRef } from "vue";

export const useAuthStore = defineStore("role", () => {
  const accessToken: Ref<string> = ref(localStorage.getItem('access_token') ?? "");
  const userAuthenticated: ComputedRef<boolean> = computed(() => !!accessToken.value);


  function setAccessToken(newToken: string): void { 
    localStorage.setItem('access_token', newToken);
    accessToken.value = newToken;
  }

  function removeAccessToken(): void {
    localStorage.setItem('access_token', "");
    accessToken.value = "";
  }

  // you have to return every state property in order for pinia to work properly
  return {
    accessToken,
    userAuthenticated,
    setAccessToken,
    removeAccessToken,
  };
});
