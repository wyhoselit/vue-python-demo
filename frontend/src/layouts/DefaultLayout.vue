<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-toolbar-title>AI Platform</v-toolbar-title>
      <v-spacer />
      <v-btn icon @click="toggleTheme">
        <v-icon>{{ isDark ? 'mdi:weather-sunny' : 'mdi:weather-night' }}</v-icon>
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      app
      temporary
      class="d-sm-d-none"
    >
      <v-list>
        <v-list-item to="/">
          <v-list-item-title>Dashboard</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-side-navigation-drawer v-show="isDesktop" app>
      <v-list>
        <v-list-item to="/">
          <v-list-item-title>Dashboard</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-side-navigation-drawer>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useThemeStore } from '@/stores/theme'
import { useDisplay } from 'vuetify'

const drawer = ref(false)
const themeStore = useThemeStore()
const { isDark } = themeStore
const { smAndDown } = useDisplay()
const isDesktop = computed(() => !smAndDown.value)

const toggleTheme = () => {
  themeStore.toggleTheme()
}

watch(smAndDown, (value) => {
  if (!value) drawer.value = false
})
</script>

<style scoped>
.v-side-navigation-drawer {
  width: 200px;
}
</style>