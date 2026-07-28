<template>
  <div class="admin-status">
    <h1>System Status</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <p>Version: {{ systemInfo.version }}</p>
      <p>OS: {{ systemInfo.os }}</p>
      <p>Database: {{ systemInfo.database }}</p>
      
      <h2>Recent Logs</h2>
      <pre>{{ logs }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const systemInfo = ref<any>(null)
const logs = ref<string>('')
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    const [infoRes, logsRes] = await Promise.all([
      api.get('/api/v1/admin/system-info'),
      api.get('/api/v1/admin/logs')
    ])
    systemInfo.value = infoRes.data
    logs.value = logsRes.data.logs
  } catch (e: any) {
    error.value = 'Failed to load admin data'
  } finally {
    loading.value = false
  }
})
</script>
