<script setup lang="ts">
import { useAuth } from '@/composables/useAuth';
import { ref, onMounted } from 'vue'
import { fetchCurrentUser } from '../services/user'
import { useRouter } from 'vue-router'
import { useAccount } from '@/composables/useAccount'
import api from '@/services/api'

const router = useRouter()
const auth = useAuth()
const { deleteAccount } = useAccount()

const userName = ref('')
const profileImage = ref('')

const loadUser = async () => {
  console.log('[loadUser] Wird ausgeführt...')
  try {
    const fetchCurrentUser = async () => {
      const res = await api.get('/users/me')
      return res.data
    }

    const user = await fetchCurrentUser()

    userName.value = `${user.first_name} ${user.last_name}`
    profileImage.value = user.avatar_url || 'https://randomuser.me/api/portraits/lego/1.jpg'
  } catch (error) {
    console.error('Fehler beim Laden des Profils:', error)
  }
}

const actions = [
   {
    icon: '⚙️',
    text: 'Profil bearbeiten',
    onClick: () => router.push('/profile/edit')
  },
  { icon: '💰', text: 'Guthaben aufladen', onClick: () => console.log('Guthaben aufladen') },
  { icon: '🔒', text: 'Sicherheit', onClick: () => console.log('Sicherheit') },
  { icon: '🛡️', text: 'Datenschutz', onClick: () => console.log('Datenschutz') }
]

const dangerActions = [
  { icon: '🚪', text: 'Abmelden', onClick: () => auth.logout() },
  { icon: '🗑️', text: 'Konto löschen', onClick: deleteAccount }
]

onMounted(() => {
  loadUser()
})
</script>

<template>
  <div class="profile-wrapper">
    <!-- Überschrift oben links -->
    <h1 class="page-title">Profil</h1>

    <div class="profile-header">
      <div class="profile-info">
        <img :src="profileImage" alt="Profilbild" class="profile-image" />
        <h2>{{ userName }}</h2>
      </div>
    </div>

    <!-- Aktionen direkt auf der Seite -->
    <div class="action-list">
      <div
        v-for="action in actions"
        :key="action.text"
        class="profile-action"
        @click="action.onClick"
      >
        <div class="action-left">
          <span class="icon">{{ action.icon }}</span>
          <span>{{ action.text }}</span>
        </div>
        <span class="arrow">›</span>
      </div>

      <p class="danger-label">Danger Zone</p>

      <div
        v-for="danger in dangerActions"
        :key="danger.text"
        class="profile-action danger"
        @click="danger.onClick"
      >
        <div class="action-left">
          <span class="icon">{{ danger.icon }}</span>
          <span>{{ danger.text }}</span>
        </div>
        <span class="arrow">›</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-wrapper {
  padding: 2rem 1rem;
  max-width: 768px;
  margin: 0 auto;
}

/* Überschrift oben links */
.page-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
}

.profile-header {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.profile-info {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-image {
  width: 96px;
  height: 96px;
  border-radius: 9999px;
  object-fit: cover;
  margin-bottom: 0.5rem;
}

h2 {
  font-size: 1.2rem;
  font-weight: 600;
}

.action-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}

.profile-action {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
  cursor: pointer;
}

.profile-action:hover {
  background-color: #f3f4f6;
}

.action-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.icon {
  font-size: 1.25rem;
}

.arrow {
  font-size: 1.25rem;
  color: #9ca3af;
}

.danger-label {
  color: #dc2626;
  font-weight: 600;
  margin-top: 1rem;
}

.danger {
  color: #dc2626;
  border-color: #fecaca;
  background-color: #fef2f2;
}
</style>
