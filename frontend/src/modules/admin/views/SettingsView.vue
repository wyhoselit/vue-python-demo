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
      <div class="setting-item">
        <label>
          Logfile Path:
          <input type="text" v-model="logfilePath" @change="updateLogfilePath" />
        </label>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getTracingConfig, updateTracingConfig } from '@/modules/admin/tracing-endpoints'
import { getSystemConfig, updateSystemConfig } from '@/modules/admin/config-endpoints'

const tracingEnabled = ref<boolean>(false)
const logfilePath = ref<string>('')
const loading = ref(true)
const error = ref<string | null>(null)

const toggleTracing = async () => {
  try {
    const data = await updateTracingConfig(tracingEnabled.value)
    tracingEnabled.value = data.enabled
  } catch (e: any) {
    error.value = 'Failed to update tracing configuration'
  }
}

const updateLogfilePath = async () => {
  try {
    const data = await updateSystemConfig('system.logfile_path', { path: logfilePath.value })
    logfilePath.value = data.path
  } catch (e: any) {
    error.value = 'Failed to update logfile path'
  }
}

onMounted(async () => {
  try {
    const [tracing, logfile] = await Promise.all([
      getTracingConfig(),
      getSystemConfig('system.logfile_path')
    ])
    tracingEnabled.value = tracing.enabled
    logfilePath.value = logfile.path
  } catch (e: any) {
    error.value = 'Failed to load configuration'
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
