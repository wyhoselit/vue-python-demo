<template>
  <v-app>
    <v-main>
      <v-container class="fill-height pa-12">
        <v-row justify="center" align="center">
          <v-col cols="12" sm="8" md="4">
            <router-view />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
// AuthLayout - minimal layout for login/register pages
// No app-bar, no navigation drawer, just centered content
</script>