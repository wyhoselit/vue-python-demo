<template>
  <div class="admin-status">
    <h1>System Information</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <p>Version: {{ systemInfo.version }}</p>
      <p>OS: {{ systemInfo.os }}</p>
      <p>Database: {{ systemInfo.database }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/shared/api'

const systemInfo = ref<any>(null)
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    const response = await api.get('/api/v1/admin/system-info')
    systemInfo.value = response.data
  } catch (e: any) {
    error.value = 'Failed to load system information'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.admin-status {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}
</style>
