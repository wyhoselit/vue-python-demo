<template>
  <div class="admin-settings">
    <h1>System Settings</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <div class="setting-item" v-for="(setting, key) in settings" :key="key">
        <label>
          <span class="setting-key">{{ key }}</span>
          <SettingControl :setting="{ ...setting, key }" @update="updateSetting" />
        </label>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getAllConfig, updateSystemConfig } from '@/modules/admin/config-endpoints'
import SettingControl from '../components/SettingControl.vue'

interface Setting {
  type: 'string' | 'boolean' | 'number' | 'object'
  value: any
}

const settings = ref<Record<string, Setting>>({})
const loading = ref(true)
const error = ref<string | null>(null)

const updateSetting = async (key: string, value: any) => {
  try {
    await updateSystemConfig(key, value)
    settings.value[key].value = value
  } catch (e: any) {
    error.value = `Failed to update ${key}: ${e.message}`
  }
}

const loadSettings = async () => {
  try {
    const data = await getAllConfig()
    const parsed: Record<string, Setting> = {}
    for (const [key, item] of Object.entries(data)) {
      parsed[key] = item as Setting
    }
    settings.value = parsed
  } catch (e: any) {
    error.value = 'Failed to load configuration'
  } finally {
    loading.value = false
  }
}

onMounted(loadSettings)
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

.setting-key {
  display: block;
  font-weight: 600;
  margin-bottom: 8px;
  font-family: monospace;
  font-size: 0.9em;
}

.setting-control {
  display: flex;
  align-items: center;
  gap: 10px;
}

.setting-control input[type="checkbox"] {
  width: 1.25rem;
  height: 1.25rem;
}

.setting-control input[type="text"],
.setting-control input[type="number"],
.setting-control textarea {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-family: inherit;
}

.setting-control textarea {
  min-height: 80px;
  resize: vertical;
  font-family: monospace;
}
</style>