<script setup lang="ts">
import { useAuth } from '@/composables/useAuth'
import { ref, onMounted } from 'vue'
import { fetchCurrentUser } from '../services/user'
import { useRouter } from 'vue-router'
import { useAccount } from '@/composables/useAccount'
import PageTitle from '@/components/PageTitle.vue'
import { useToaster } from '@/composables/useToaster'

// Lucide Icons
import { Settings, Wallet, Lock, Shield, LogOut, Trash2 } from 'lucide-vue-next'

const router = useRouter()
const auth = useAuth()
const { deleteAccount } = useAccount()
const { showToast } = useToaster()

const firstName = ref('')
const lastName = ref('')
const profileImage = ref('')

const loadUser = async () => {
  try {
    const user = await fetchCurrentUser()
    firstName.value = user.first_name
    lastName.value = user.last_name
    profileImage.value = user.avatar_url || 'https://randomuser.me/api/portraits/lego/1.jpg'
  } catch {
    showToast('error', 'Fehler beim Laden des Profils')
  }
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
    onClick: () => console.log('Guthaben aufladen')
  },
  {
    icon: Lock,
    isComponent: true,
    text: 'Sicherheit',
    onClick: () => console.log('Sicherheit')
  },
  {
    icon: Shield,
    isComponent: true,
    text: 'Datenschutz',
    onClick: () => console.log('Datenschutz')
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
    onClick: deleteAccount
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
      <img :src="profileImage" alt="Profilbild" class="profile-image" />
      <h2 class="user-name">{{ firstName }} {{ lastName }}</h2>
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
        <span class="arrow">›</span>
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
        <span class="arrow">›</span>
      </div>
    </div>
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
  width: 96px;
  height: 96px;
  border-radius: 9999px;
  object-fit: cover;
  margin-bottom: 0.5rem;
}

.user-name {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-neutral-900);
}

.action-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
}

.profile-action {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border-radius: var(--border-radius);
  background-color: var(--color-neutral-200);
  border: 1px solid var(--color-neutral-300);
  cursor: pointer;
  transition: background-color 0.2s;
}

.profile-action:hover {
  background-color: var(--color-neutral-300);
}

.action-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.icon {
  height: 20px;
  width: 20px;
  color: var(--color-neutral-900);
}

.arrow {
  font-size: 1.25rem;
  color: var(--color-neutral-400);
}

.text {
  color: var(--color-neutral-900);
  font-weight: var(--font-weight-semibold);
}

.danger-label {
  color: var(--color-support-danger-500);
  font-weight: 600;
  margin-top: 1rem;
}

.danger {
  color: var(--color-support-danger-500);
  background-color: var(--color-support-danger-500-transparent);
  border-color: var(--color-support-danger-500-transparent);
}
</style>
