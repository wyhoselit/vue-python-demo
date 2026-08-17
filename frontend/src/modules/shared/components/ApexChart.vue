<template>
  <v-card outlined>
    <v-card-title>{{ title }}</v-card-title>
    <v-card-text>
      <div :id="chartId"></div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import ApexCharts, {
  ApexAxisChartSeries,
  ApexNonAxisChartSeries,
  ApexOptions,
} from 'apexcharts'

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  chartId: {
    type: String,
    required: true,
  },
  series: {
    type: Array as () => ApexAxisChartSeries | ApexNonAxisChartSeries,
    required: true,
  },
  chartOptions: {
    type: Object as () => ApexOptions,
    required: true,
  },
})

const chart = ref<ApexCharts | null>(null)

onMounted(() => {
  const element = document.getElementById(props.chartId)
  if (!element) return
  chart.value = new ApexCharts(element, {
    series: props.series,
    chart: props.chartOptions.chart,
    ...props.chartOptions,
  })
  chart.value.render()
})

watch(() => props.series, (newSeries) => {
  if (chart.value) {
    chart.value.updateSeries(newSeries)
  }
}, { deep: true })

watch(() => props.chartOptions, (newOptions) => {
  if (chart.value) {
    chart.value.updateOptions(newOptions)
  }
}, { deep: true })
</script>
