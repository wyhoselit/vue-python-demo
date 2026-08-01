<template>
  <v-card class="auth-form" elevation="8">
    <v-card-title class="auth-form__title">
      <v-icon left mdi:login /> Sign In
    </v-card-title>
    
    <v-card-text>
      <v-form ref="form" @submit.prevent="onSubmit">
        <v-text-field
          v-model="email"
          type="email"
          label="Email"
          placeholder="you@example.com"
          prepend-inner-icon="mdi:email"
          required
          :rules="[v => !!v || 'Email is required']"
        />
        
        <v-text-field
          v-model="password"
          type="password"
          label="Password"
          prepend-inner-icon="mdi:lock"
          required
          :rules="[v => !!v || 'Password is required']"
        />
        
        <v-alert
          v-if="authStore.error"
          type="error"
          variant="tonal"
          class="mb-4"
        >
          {{ authStore.error }}
        </v-alert>
        
        <v-btn
          type="submit"
          color="primary"
          :loading="authStore.loading"
          :disabled="authStore.loading"
          block
        >
          Sign In
        </v-btn>
      </v-form>
      
      <v-divider class="my-4" />
      
      <v-btn
        variant="text"
        @click="router.push('/register')"
      >
        Don't have an account? Register
      </v-btn>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')

const onSubmit = async () => {
  try {
    await authStore.login({
      email: email.value,
      password: password.value
    })
    router.push('/dashboard')
  } catch (e) {
    // Error is handled in authStore
  }
}
</script>

<style scoped>
.auth-form {
  max-width: 400px;
  margin: 2rem auto;
}

.auth-form__title {
  font-size: 1.5rem;
  font-weight: 600;
}
</style>