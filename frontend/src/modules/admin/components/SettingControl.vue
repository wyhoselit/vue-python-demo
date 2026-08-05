<template>
  <div class="setting-control">
    <input 
      v-if="setting.type === 'boolean'" 
      type="checkbox" 
      :checked="setting.value" 
      @change="$emit('update', setting.key, ($event.target as HTMLInputElement).checked)"
    />
    <input 
      v-else-if="setting.type === 'number'" 
      type="number" 
      :value="setting.value" 
      @change="$emit('update', setting.key, Number(($event.target as HTMLInputElement).value))"
    />
    <textarea 
      v-else-if="setting.type === 'object'" 
      :value="JSON.stringify(setting.value, null, 2)"
      @blur="$emit('update', setting.key, tryParseJSON(($event.target as HTMLTextAreaElement).value))"
    />
    <input 
      v-else 
      type="text" 
      :value="setting.value" 
      @change="$emit('update', setting.key, ($event.target as HTMLInputElement).value)"
    />
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ setting: { type: string, value: any, key: string } }>()

const tryParseJSON = (value: string) => {
  try {
    return JSON.parse(value)
  } catch (e) {
    return value
  }
}

defineEmits(['update'])
</script>

<style scoped>
.setting-control {
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>