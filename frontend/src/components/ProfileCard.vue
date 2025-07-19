<script setup lang="ts">
import type { ProfileCardProps } from '@/types/Props';
import { Star } from 'lucide-vue-next'

const props = defineProps<ProfileCardProps>()

const getStarIcons = (value: number) => {
  const stars = []
  for (let i = 1; i <= 5; i++) {
    if (value >= i) stars.push({ type: 'full' })
    else if (value >= i - 0.5) stars.push({ type: 'half' })
    else stars.push({ type: 'empty' })
  }
  return stars
}
</script>

<template>
  <div class="driver-card">
    <img :src="props.profile_picture" alt="Profilbild" class="profile-img" />
    <div class="driver-details">
      <p class="text-bold text-xl margin-bottom-s">{{ props.first_name }} {{ props.last_name }}</p>
      <div class="rating-stars">
        <component
          v-for="(star, index) in getStarIcons(props.avg_rating ?? 0)"
          :key="index"
          :is="Star"
          class="icon-xs"
          :style="{
            fill: star.type === 'full' ? 'black' : star.type === 'half' ? 'url(#half)' : 'none',
            stroke: 'black'
          }"
        />
        <svg width="0" height="0">
          <defs>
            <linearGradient id="half" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="50%" stop-color="black" />
              <stop offset="50%" stop-color="white" stop-opacity="1" />
            </linearGradient>
          </defs>
        </svg>
      </div>
    </div>
  </div>
</template>

<style scoped>
.driver-card {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  margin: 0 auto;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  background-color: #f7f5fb;
  gap: 1rem;
  max-width: 600px;
  width: 100%;
}
.driver-details {
  display: flex;
  flex-direction: column;
}
.name {
  font-size: 1.1rem;
}
.rating-stars {
  display: flex;
  gap: 0.25rem;
  margin-top: 0.25rem;
}
.profile-img {
  width: var(--profile-picture-md-dim);
  height: var(--profile-picture-md-dim);
  border-radius: 9999px;
  object-fit: cover;
}
</style> 