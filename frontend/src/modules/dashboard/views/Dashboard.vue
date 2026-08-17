<template>
  <v-container>
    <!-- Loading State -->
    <v-row dense v-if="loading" justify="center">
      <v-col cols="12" class="text-center py-12">
        <v-progress-circular indeterminate size="64" color="primary" />
        <span class="d-block mt-4 text-subtitle-1">載入儀表板資料中...</span>
      </v-col>
    </v-row>

    <!-- Error State -->
    <v-row dense v-else-if="error" justify="center">
      <v-col cols="12" md="8">
        <v-alert type="error" dismissible @click:close="error = null">
          <strong>載入失敗：</strong> {{ error }}
          <template v-slot:append>
            <v-btn variant="text" @click="fetchData">重試</v-btn>
          </template>
        </v-alert>
      </v-col>
    </v-row>

    <!-- Dashboard Content -->
    <v-row dense v-else>
      <v-col cols="12" md="4" v-for="card in statsCards" :key="card.title">
        <v-card outlined>
          <v-card-title class="text-h6">{{ card.title }}</v-card-title>
          <v-card-text>
            <div class="text-h4">{{ card.formattedValue }}</div>
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
          <v-card-title>使用者列表</v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="users"
              class="elevation-1"
              :items-per-page="10"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useApi } from '@/shared/useApi'
import { useComponentRenderMetrics } from '@/modules/core/metrics/useComponentRenderMetrics'

useComponentRenderMetrics()

// 型別定義
interface DashboardStats {
  total_users: number
  active_sessions: number
  api_calls_24h: number
}

interface User {
  id: number
  name: string
  email: string
  status: string
}

interface StatCard {
  title: string
  value: number
  progress?: number
  formattedValue: string
}

const loading = ref(true)
const error = ref<string | null>(null)
const stats = ref<DashboardStats | null>(null)
const users = ref<User[]>([])

const api = useApi()

const headers = [
  { title: 'ID', key: 'id' },
  { title: '姓名', key: 'name' },
  { title: 'Email', key: 'email' },
  { title: '狀態', key: 'status' },
]

const statsCards = computed<StatCard[]>(() => {
  if (!stats.value) return []
  return [
    {
      title: '總用戶數',
      value: stats.value.total_users,
      formattedValue: stats.value.total_users.toLocaleString(),
    },
    {
      title: '活躍會話',
      value: stats.value.active_sessions,
      formattedValue: stats.value.active_sessions.toLocaleString(),
    },
    {
      title: 'API 呼叫 (24h)',
      value: stats.value.api_calls_24h,
      formattedValue: stats.value.api_calls_24h.toLocaleString(),
    },
  ]
})

const fetchStats = async (): Promise<DashboardStats> => {
  const data = await api.get<DashboardStats>('/dashboard/stats')
  return data
}

const fetchUsers = async (): Promise<User[]> => {
  const data = await api.get<User[]>('/users')
  return data
}

const fetchData = async () => {
  loading.value = true
  error.value = null

  try {
    const [statsData, usersData] = await Promise.all([
      fetchStats(),
      fetchUsers(),
    ])
    stats.value = statsData
    users.value = usersData
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : '未知錯誤'
    error.value = `無法載入儀表板資料：${message}`
    console.error('Failed to fetch dashboard data:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>