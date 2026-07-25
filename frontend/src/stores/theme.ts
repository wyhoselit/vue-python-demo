import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref(false)

  const theme = computed(() => (isDark.value ? 'dark' : 'light'))

  const toggleTheme = () => {
    isDark.value = !isDark.value
    localStorage.setItem('theme', theme.value)
    applyTheme()
  }

  const initTheme = () => {
    const saved = localStorage.getItem('theme') as 'light' | 'dark' | null
    if (saved) {
      isDark.value = saved === 'dark'
    } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      isDark.value = true
    }
    applyTheme()
  }

  const applyTheme = () => {
    document.documentElement.setAttribute('data-theme', theme.value)
  }

  return {
    isDark,
    theme,
    toggleTheme,
    initTheme,
  }
})