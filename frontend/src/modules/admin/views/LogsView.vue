<template>
  <div class="admin-logs">
    <h1>Recent Logs</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <pre>{{ logs }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/shared/api'

const logs = ref<string>('')
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    const response = await api.get('/api/v1/admin/logs')
    logs.value = response.data.logs
  } catch (e: any) {
    error.value = 'Failed to load logs'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.admin-logs {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  font-family: monospace;
  background-color: #f5f5f5;
  border-radius: 4px;
  overflow: hidden;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  padding: 15px;
  margin: 0;
  background-color: #fff;
  border-radius: 4px;
  max-height: 400px;
  overflow-y: auto;
}
</style>
