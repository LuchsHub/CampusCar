<script setup lang="ts">
</script>

<template>
  <div class="profile-edit-wrapper">
    <PageTitle>Profil bearbeiten</PageTitle>

    <div class="placeholder-box">
      <p>🛠️ Hier wird gerade dran gearbeitet</p>
    </div>
  </div>
</template>

<style scoped>
.profile-edit-wrapper {
  padding: 2rem 1rem;
  max-width: 768px;
  margin: 0 auto;
  background-color: white;
  min-height: 100vh;
}

.page-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 2rem;
}

.placeholder-box {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 300px;
  border: 2px dashed #d1d5db;
  border-radius: 12px;
  background-color: #f9fafb;
  font-size: 1rem;
  color: #6b7280;
}
</style>
