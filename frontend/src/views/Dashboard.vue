<template>
  <v-container>
    <v-row dense>
      <v-col cols="12" md="4" v-for="card in cards" :key="card.title">
        <v-card outlined>
          <v-card-title class="text-h6">{{ card.title }}</v-card-title>
          <v-card-text>
            <div class="text-h4" v-if="card.value !== undefined">
              {{ card.value }}
            </div>
            <v-progress-linear
              v-if="card.progress !== undefined"
              :value="card.progress"
              color="primary"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row dense>
      <v-col cols="12">
        <v-card outlined>
          <v-card-title>Data Table</v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="items"
              class="elevation-1"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'

const cards = ref([
  { title: 'Total Users', value: 0, progress: 0 },
  { title: 'Active Sessions', value: 0, progress: 0 },
  { title: 'API Calls (24h)', value: 0, progress: 0 },
])

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Name', key: 'name' },
  { title: 'Email', key: 'email' },
  { title: 'Status', key: 'status' },
]

const items = ref<Array<{ id: number; name: string; email: string; status: string }>>([])

const api = useApi()

const fetchData = async () => {
  try {
    const data = await api.get<{
      cards: { title: string; value: number; progress: number }[]
      users: { id: number; name: string; email: string; status: string }[]
    }>('/dashboard')
    cards.value = data.cards || cards.value
    items.value = data.users || items.value
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
  }
}

onMounted(() => {
  fetchData()
})
</script>