<template>
  <div class="admin-status">
    <h1>System Status</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <p>Version: {{ systemInfo.version }}</p>
      <p>OS: {{ systemInfo.os }}</p>
      <p>Database: {{ systemInfo.database }}</p>
      
      <h2>Tracing Configuration</h2>
      <div class="tracing-config">
        <label class="toggle-label">
          <input type="checkbox" v-model="tracingEnabled" @change="toggleTracing" />
          <span>Enable Tracing</span>
        </label>
        <p class="tracing-status">Current status: {{ tracingEnabled ? 'Enabled' : 'Disabled' }}</p>
      </div>
      
      <h2>Recent Logs</h2>
      <pre>{{ logs }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/shared/api'

const systemInfo = ref<any>(null)
const logs = ref<string>('')
const tracingEnabled = ref<boolean>(false)
const loading = ref(true)
const error = ref<string | null>(null)

const toggleTracing = async () => {
  try {
    const response = await api.put('/api/v1/admin/tracing/config', { enabled: tracingEnabled.value })
    tracingEnabled.value = response.data.enabled
  } catch (e: any) {
    error.value = 'Failed to update tracing configuration'
  }
}

onMounted(async () => {
  try {
    const [infoRes, logsRes, traceRes] = await Promise.all([
      api.get('/api/v1/admin/system-info'),
      api.get('/api/v1/admin/logs'),
      api.get('/api/v1/admin/tracing/config')
    ])
    systemInfo.value = infoRes.data
    logs.value = logsRes.data.logs
    tracingEnabled.value = traceRes.data.enabled
  } catch (e: any) {
    error.value = 'Failed to load admin data'
  } finally {
    loading.value = false
  }
})
</script>
