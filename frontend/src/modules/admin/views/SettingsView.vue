<template>
  <div class="admin-settings">
    <h1>System Settings</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <div class="setting-item">
        <label class="toggle-label">
          <input type="checkbox" v-model="tracingEnabled" @change="toggleTracing" />
          <span>Enable Tracing</span>
        </label>
        <p class="tracing-status">Current status: {{ tracingEnabled ? 'Enabled' : 'Disabled' }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/shared/api'

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
    const response = await api.get('/api/v1/admin/tracing/config')
    tracingEnabled.value = response.data.enabled
  } catch (e: any) {
    error.value = 'Failed to load tracing configuration'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.admin-settings {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.setting-item {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.tracing-status {
  margin-top: 5px;
  font-size: 0.9em;
  color: #666;
}
</style>
