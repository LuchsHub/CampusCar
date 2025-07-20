<script setup lang="ts">
import HoverButton from '@/components/HoverButton.vue';
import PageTitle from '@/components/PageTitle.vue';
import { computed, onMounted, ref } from 'vue';
import { useUser } from '@/composables/useUser';
import { useToaster } from '@/composables/useToaster';
import TabSwitcher from '@/components/TabSwitcher.vue';
import type { BonusGet } from '@/types/Bonus';
import { useBonus } from '@/composables/useBonus';
import BonusCard from '@/components/BonusCard.vue';

const { getUserPoints } = useUser(); 
const { showToast } = useToaster();
const { getAllBonuses, getUsersBonuses, redeemBonus } = useBonus();

type bonusTabs = 'Einlösen' | 'Bereits erhalten';
const activeTab = ref<bonusTabs>('Einlösen');
const tabs: bonusTabs[] = ['Einlösen', 'Bereits erhalten'];

const loading = ref<boolean>(false);
const userPoints = ref<number>(0);
const userHasEnoughPoints = ref<boolean>(false);

const allBonuses = ref<BonusGet[]>([]);
const userBonuses = ref<BonusGet[]>([]);

const userBonusesWithCount = computed(() => {
  const bonusMap = new Map<string, BonusGet & { count: number }>();

  for (const bonus of userBonuses.value) {
    const entry = bonusMap.get(bonus.name);
    if (entry) {
      entry.count = Number(entry.count) + 1;
    } else {
      bonusMap.set(bonus.name, { ...bonus, count: 1 });
    }
  }

  return Array.from(bonusMap.values());
});

const selectedBonus = ref<BonusGet | null>(null);

onMounted(async () => {
  userPoints.value = await getUserPoints();
  allBonuses.value = await getAllBonuses();
  userBonuses.value = await getUsersBonuses();
})

const selectBonus = (bonus: BonusGet) => {
  selectedBonus.value = bonus;
  userHasEnoughPoints.value = selectedBonus.value.cost <= userPoints.value;
};

const onRedeemBonus = async () => {

  if (!selectedBonus.value) {
    showToast('error', 'Wähle zuerst eine Prämie aus.');
    return;
  }

  try {
    loading.value = true;
    await redeemBonus(selectedBonus.value?.id);
    showToast('success', `Prämie erhalten: ${selectedBonus.value?.name}`);
    userBonuses.value = await getUsersBonuses();
    activeTab.value = 'Bereits erhalten';
  } catch (error:unknown) {
    showToast("error", "Du hast nicht genug Punkte.");
    console.log(error);
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="view-container padding-bottom-hb-1">
    <PageTitle :goBack="true">Prämien</PageTitle>

    <TabSwitcher v-model="activeTab" :tabs="tabs" />

    <div v-if="activeTab === 'Einlösen'" class="width-100 component-list">
      <p class="text-semibold">Du hast aktuell <span class="text-primary text-l">{{ userPoints }}</span> Punkte.</p>
      <template v-for="(bonus, _) in allBonuses" :key="bonus.id">
        <BonusCard 
          :bonus="bonus"
          :selected="selectedBonus?.id === bonus.id"
          :isRedeemed="false"
          @click="selectBonus(bonus)"
        />
      </template>
      <p v-if="allBonuses.length === 0" class="text-semibold">Momentan sind keine Prämien verfügbar. Versuche es später nochmal.</p>
      <div v-if="!userHasEnoughPoints && selectedBonus" class="margin-botton-l error-message-container">
        <p class="text-danger">Du hast nicht genügend Punkte, um diese Prämie zu erwerben. Erstelle mehr Fahrten, um mehr Punkte zu sammeln!</p>
    </div>
    </div>
      
    <div v-else class="width-100 component-list">
      <template v-for="(bonus, _) in userBonusesWithCount" :key="bonus.id">
        <BonusCard
        :bonus="bonus"
        :isRedeemed="true"
        />
      </template>
      <p v-if="userBonusesWithCount.length === 0" class="text-semibold">Du hast aktuell noch keine Prämien eingelöst. Erstelle Fahrten und sammle Punkte, um Prämien zu erhalten.</p>
    </div>

    <HoverButton v-if="activeTab === 'Einlösen'" :buttons='[
      {variant: "primary", onClick: onRedeemBonus, text: "Prämie anfordern", disabled: (!selectedBonus || !userHasEnoughPoints), loading: loading}]'
    />
  </div>
</template>

<style scoped>
</style>