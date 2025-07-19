import { computed, ref } from "vue";
import { defineStore } from "pinia";
import type { Ref, ComputedRef } from "vue";

export const useAuthStore = defineStore("role", () => {
  const accessToken: Ref<string> = ref(localStorage.getItem('access_token') ?? "");
  const userId: Ref<string> = ref(localStorage.getItem('user_id') ?? "");
  const userAuthenticated: ComputedRef<boolean> = computed(() => !!accessToken.value);

  function setAccessToken(newToken: string): void { 
    localStorage.setItem('access_token', newToken);
    accessToken.value = newToken;
  }

  function removeAccessToken(): void {
    localStorage.setItem('access_token', "");
    accessToken.value = "";
  }
  
  function setUserId(newId: string): void { 
    localStorage.setItem('user_id', newId);
    userId.value = newId;
  }

  function removeUserId(): void {
    localStorage.setItem('user_id', "");
    userId.value = "";
  }

  // you have to return every state property in order for pinia to work properly
  return {
    accessToken,
    userId,
    userAuthenticated,
    setAccessToken,
    removeAccessToken,
    setUserId,
    removeUserId
  };
});
