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

    <!-- Real-time Charts -->
    <v-row dense>
      <v-col cols="12" md="6">
        <ApexChart
          :chartId="realtimeChartId"
          title="即時 API 請求趨勢"
          :series="realtimeSeries"
          :chartOptions="realtimeChartOptions"
        />
      </v-col>
      <v-col cols="12" md="6">
        <ApexChart
          :chartId="distributionChartId"
          title="API 回應時間分佈"
          :series="distributionSeries"
          :chartOptions="distributionChartOptions"
        />
      </v-col>
    </v-row>

    <v-row dense>
      <v-col cols="12" md="6">
        <ApexChart
          :chartId="statusChartId"
          title="API 狀態碼分佈"
          :series="statusSeries"
          :chartOptions="statusChartOptions"
        />
      </v-col>
      <v-col cols="12" md="6">
        <ApexChart
          :chartId="usersChartId"
          title="活躍用戶趨勢"
          :series="usersSeries"
          :chartOptions="usersChartOptions"
        />
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
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useApi } from '@/shared/useApi'
import { useComponentRenderMetrics } from '@/modules/core/metrics/useComponentRenderMetrics'
import ApexChart from '@/modules/shared/components/ApexChart.vue'

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

interface RealtimeDataPoint {
  timestamp: string
  requests: number
  avgResponseTime: number
  status2xx: number
  status4xx: number
  status5xx: number
  activeUsers: number
}

const loading = ref(true)
const error = ref<string | null>(null)
const stats = ref<DashboardStats | null>(null)
const users = ref<User[]>([])
const realtimeData = ref<RealtimeDataPoint[]>([])

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

const realtimeChartId = 'realtime-chart'
const distributionChartId = 'distribution-chart'
const statusChartId = 'status-chart'
const usersChartId = 'users-chart'

const realtimeSeries = computed(() => [
  {
    name: 'API 請求數',
    data: realtimeData.value.map((d, i) => [i, d.requests]),
  },
])

const distributionSeries = computed(() => [
  {
    name: '平均回應時間 (ms)',
    data: realtimeData.value.map((d, i) => [i, d.avgResponseTime]),
  },
])

const statusSeries = computed(() => [
  realtimeData.value.length > 0
    ? realtimeData.value[realtimeData.value.length - 1].status2xx
    : 0,
  realtimeData.value.length > 0
    ? realtimeData.value[realtimeData.value.length - 1].status4xx
    : 0,
  realtimeData.value.length > 0
    ? realtimeData.value[realtimeData.value.length - 1].status5xx
    : 0,
])

const usersSeries = computed(() => [
  {
    name: '活躍用戶',
    data: realtimeData.value.map((d, i) => [i, d.activeUsers]),
  },
])

const realtimeChartOptions = computed(() => ({
  chart: {
    type: 'area' as const,
    height: 300,
    toolbar: { show: false },
    animations: { enabled: true, easing: 'linear', dynamicAnimation: { enabled: true, speed: 1000 } },
  },
  dataLabels: { enabled: false },
  stroke: { curve: 'smooth' as const, width: 2 },
  xaxis: {
    type: 'category' as const,
    categories: realtimeData.value.map((_, i) => i.toString()),
    labels: { show: false },
  },
  yaxis: {
    title: { text: '請求數' },
  },
  tooltip: {
    x: {
      formatter: (val: number) => `第 ${val + 1} 個間隔`,
    },
  },
  colors: ['#3f51b5'],
  fill: {
    type: 'gradient' as const,
    gradient: {
      shadeIntensity: 1,
      opacityFrom: 0.4,
      opacityTo: 0.1,
      stops: [0, 90, 100],
    },
  },
}))

const distributionChartOptions = computed(() => ({
  chart: {
    type: 'line' as const,
    height: 300,
    toolbar: { show: false },
    animations: { enabled: true },
  },
  dataLabels: { enabled: false },
  stroke: { curve: 'smooth' as const, width: 2 },
  xaxis: {
    type: 'category' as const,
    categories: realtimeData.value.map((_, i) => i.toString()),
    labels: { show: false },
  },
  yaxis: {
    title: { text: '毫秒' },
  },
  colors: ['#ff9800'],
}))

const statusChartOptions = computed(() => ({
  chart: {
    type: 'donut' as const,
    height: 300,
  },
  labels: ['2xx 成功', '4xx 客戶端錯誤', '5xx 伺服器錯誤'],
  colors: ['#4caf50', '#ff9800', '#f44336'],
  legend: { position: 'bottom' as const },
  dataLabels: { enabled: true },
}))

const usersChartOptions = computed(() => ({
  chart: {
    type: 'bar' as const,
    height: 300,
    toolbar: { show: false },
    animations: { enabled: true },
  },
  dataLabels: { enabled: false },
  xaxis: {
    type: 'category' as const,
    categories: realtimeData.value.map((_, i) => i.toString()),
    labels: { show: false },
  },
  yaxis: {
    title: { text: '用戶數' },
  },
  colors: ['#2196f3'],
}))

const fetchStats = async (): Promise<DashboardStats> => {
  const data = await api.get<DashboardStats>('/dashboard/stats')
  return data
}

const fetchUsers = async (): Promise<User[]> => {
  const data = await api.get<User[]>('/users')
  return data
}

const fetchRealtimeData = async (): Promise<RealtimeDataPoint[]> => {
  try {
    const data = await api.get<RealtimeDataPoint[]>('/dashboard/realtime')
    return data
  } catch {
    return []
  }
}

const fetchData = async () => {
  loading.value = true
  error.value = null

  try {
    const [statsData, usersData, realtimeDataRes] = await Promise.all([
      fetchStats(),
      fetchUsers(),
      fetchRealtimeData(),
    ])
    stats.value = statsData
    users.value = usersData
    realtimeData.value = realtimeDataRes.length > 0 ? realtimeDataRes : generateMockRealtimeData()
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : '未知錯誤'
    error.value = `無法載入儀表板資料：${message}`
    console.error('Failed to fetch dashboard data:', err)
    realtimeData.value = generateMockRealtimeData()
  } finally {
    loading.value = false
  }
}

const generateMockRealtimeData = (): RealtimeDataPoint[] => {
  const now = new Date()
  const data: RealtimeDataPoint[] = []
  for (let i = 0; i < 20; i++) {
    const time = new Date(now.getTime() - (19 - i) * 30000)
    data.push({
      timestamp: time.toISOString(),
      requests: Math.floor(Math.random() * 100) + 50,
      avgResponseTime: Math.floor(Math.random() * 200) + 50,
      status2xx: Math.floor(Math.random() * 80) + 80,
      status4xx: Math.floor(Math.random() * 15) + 5,
      status5xx: Math.floor(Math.random() * 5),
      activeUsers: Math.floor(Math.random() * 30) + 20,
    })
  }
  return data
}

let intervalId: ReturnType<typeof setInterval>

const startRealtimeUpdates = () => {
  intervalId = setInterval(async () => {
    try {
      const newData = await fetchRealtimeData()
      if (newData.length > 0) {
        realtimeData.value = [...realtimeData.value.slice(-19), newData[0]]
      } else {
        // Simulate real-time update
        const lastPoint = realtimeData.value[realtimeData.value.length - 1]
        if (lastPoint) {
          realtimeData.value = [
            ...realtimeData.value.slice(1),
            {
              timestamp: new Date().toISOString(),
              requests: Math.max(10, lastPoint.requests + Math.floor(Math.random() * 20) - 10),
              avgResponseTime: Math.max(20, lastPoint.avgResponseTime + Math.floor(Math.random() * 30) - 15),
              status2xx: Math.max(50, lastPoint.status2xx + Math.floor(Math.random() * 10) - 5),
              status4xx: Math.max(0, lastPoint.status4xx + Math.floor(Math.random() * 5) - 2),
              status5xx: Math.max(0, lastPoint.status5xx + Math.floor(Math.random() * 2) - 1),
              activeUsers: Math.max(5, lastPoint.activeUsers + Math.floor(Math.random() * 5) - 2),
            },
          ]
        }
      }
    } catch {
      // Silently fail and keep mock data
    }
  }, 5000)
}

const stopRealtimeUpdates = () => {
  if (intervalId) {
    clearInterval(intervalId)
  }
}

onMounted(() => {
  fetchData()
  startRealtimeUpdates()
})

onUnmounted(() => {
  stopRealtimeUpdates()
})
</script>