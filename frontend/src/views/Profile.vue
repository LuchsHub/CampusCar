<script setup lang="ts">
import { useAuth } from '@/composables/useAuth'
import { ref, onMounted } from 'vue'
import { fetchCurrentUser } from '../services/user'
import { useRouter } from 'vue-router'
import { useAccount } from '@/composables/useAccount'
import PageTitle from '@/components/PageTitle.vue'
import { useToaster } from '@/composables/useToaster'
import ConfirmDeleteModal from '@/components/ConfirmDeleteModal.vue'
import { useUser } from '@/composables/useUser'
import { useAuthStore } from '@/stores/AuthStore'

// Lucide Icons
import {
  Settings, Wallet, Lock, Shield,
  LogOut, Trash2, ChevronRight, Star, TicketCheck
} from 'lucide-vue-next'

const router = useRouter()
const auth = useAuth()
const authStore = useAuthStore();
const { deleteAccount } = useAccount()
const { showToast } = useToaster()
const { getProfileImageUrl } = useUser()

const firstName = ref('')
const lastName = ref('')
const profileImage = ref('')
const rating = ref(0)
const showDeleteConfirm = ref(false)

const loadUser = async () => {
  try {
    const user = await fetchCurrentUser()
    firstName.value = user.first_name
    lastName.value = user.last_name

    const imageUrl = await getProfileImageUrl(authStore.userId)
    profileImage.value = imageUrl ?? ""

    rating.value = user.avg_rating ?? 0
  } catch {
    showToast('error', 'Fehler beim Laden des Profils')
  }
}

const getStarIcons = (value: number) => {
  const stars = []
  for (let i = 1; i <= 5; i++) {
    if (value >= i) {
      stars.push({ type: 'full' })
    } else if (value >= i - 0.5) {
      stars.push({ type: 'half' })
    } else {
      stars.push({ type: 'empty' })
    }
  }
  return stars
}

const actions = [
  {
    icon: Settings,
    isComponent: true,
    text: 'Profil bearbeiten',
    onClick: () => router.push('/profile/edit')
  },
  {
    icon: Wallet,
    isComponent: true,
    text: 'Guthaben aufladen',
    onClick: () => router.push('/profile/balance')
  },
  {
    icon: TicketCheck,
    isComponent: true,
    text: 'Prämien',
    onClick: () => router.push('/profile/bonus/redeem')
  },
  {
    icon: Lock,
    isComponent: true,
    text: 'Sicherheit',
    onClick: () => showToast('info', 'Dieses Feature ist nicht implementiert.')
  },
  {
    icon: Shield,
    isComponent: true,
    text: 'Datenschutz',
    onClick: () => showToast('info', 'Dieses Feature ist nicht implementiert.')
  }
]

const dangerActions = [
  {
    icon: LogOut,
    isComponent: true,
    text: 'Abmelden',
    onClick: () => auth.logoutUser()
  },
  {
    icon: Trash2,
    isComponent: true,
    text: 'Konto löschen',
    onClick: () => {
      showDeleteConfirm.value = true
    }
  }
]

onMounted(() => {
  loadUser()
})
</script>

<template>
  <div class="view-container">
    <PageTitle>Profil</PageTitle>

    <div class="profile-header">
      <img :src="profileImage" class="profile-image margin-botton-l" />
      <p class="text-xl text-bold margin-botton-l">{{ firstName }} {{ lastName }}</p>
      <div class="rating-stars margin-botton-l">
        <component
            v-for="(star, index) in getStarIcons(rating)"
            :key="index"
            :is="Star"
            class="star-icon"
            :style="{
              fill: star.type === 'full' ? 'black' : star.type === 'half' ? 'url(#half)' : 'none',
              stroke: 'black'
            }"
          />
          
          <!-- SVG Def für halben Füllbereich -->
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

    <div class="action-list">
      <div
        v-for="action in actions"
        :key="action.text"
        class="profile-action"
        @click="action.onClick"
      >
        <div class="action-left">
          <component v-if="action.isComponent" :is="action.icon" class="icon" />
          <span class="text">{{ action.text }}</span>
        </div>
        <ChevronRight class="arrow" />
      </div>

      <h2 class="danger-label">Danger Zone</h2>

      <div
        v-for="danger in dangerActions"
        :key="danger.text"
        class="profile-action danger"
        @click="danger.onClick"
      >
        <div class="action-left">
          <component v-if="danger.isComponent" :is="danger.icon" class="icon" />
          <span class="text">{{ danger.text }}</span>
        </div>
        <ChevronRight class="arrow" />
      </div>
    </div>
    <ConfirmDeleteModal
      :open="showDeleteConfirm"
      subject="Konto"
      :requiresTextConfirmation="true"
      @cancel="showDeleteConfirm = false"
      @confirm="deleteAccount"
    />
  </div>
</template>

<style scoped>
.page-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  color: var(--color-neutral-900);
}

.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
  width: 100%;
}

.profile-image {
  width: var(--profile-picture-md-dim);
  height: var(--profile-picture-md-dim);
  border-radius: 9999px;
  object-fit: cover;
}

.rating-stars {
  display: flex;
  gap: 0.25rem;
}

.star-icon {
  height: var(--icon-md);
  width: var(--icon-md);
  stroke-width: var(--line-width-m);
}

.action-list {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.profile-action {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0.5rem 0.75rem 1rem;
  border-top: none;
  border-bottom: 1px solid #d1d5db;
  background-color: transparent;
  cursor: pointer;
  transition: background-color 0.2s;
}

.profile-action:hover {
  background-color: var(--color-neutral-100);
}

.action-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.icon {
  height: 24px;
  width: 24px;
  color: var(--color-neutral-900);
  display: flex;
  align-items: center;
  justify-content: center;
}

.arrow {
  height: 24px;
  width: 24px;
  color: var(--color-neutral-900);
  display: flex;
  align-items: center;
  justify-content: center;
}

.text {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-neutral-900);
  display: flex;
  align-items: center;
}

.danger-label {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-support-danger-500);
  margin-top: 2rem;
  padding-left: 1rem;
  padding-bottom: 0.5rem;
}

.profile-action.danger {
  background-color: var(--color-support-danger-50); /* leicht roter Hintergrund */
}

.profile-action.danger:hover {
  background-color: var(--color-support-danger-100); /* dunkler beim Hover */
}

.profile-action.danger:last-of-type .icon,
.profile-action.danger:last-of-type .text,
.profile-action.danger:last-of-type .arrow {
  color: var(--color-support-danger-500);
}
</style>
