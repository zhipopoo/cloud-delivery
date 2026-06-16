<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)

async function doLogin() {
  if (!username.value || !password.value) return
  loading.value = true
  const ok = await authStore.login(username.value, password.value)
  loading.value = false
  if (ok) {
    const redirect = (route.query.redirect as string) || '/admin/members'
    router.push(redirect)
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-[#F0F2F5] hex-grid">
    <div class="geo-card w-full max-w-sm p-8 animate-slide-up">
      <!-- Logo -->
      <div class="text-center mb-6">
        <div class="flex justify-center mb-3">
          <div class="flex h-12 w-12 items-center justify-center rounded" style="background: #CE0E2D;">
            <svg class="h-6 w-6 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            </svg>
          </div>
        </div>
        <h1 class="text-lg font-extrabold tracking-tight" style="color: #1E2432;">HUAWEI CLOUD</h1>
        <p class="text-xs font-semibold uppercase tracking-[0.12em]" style="color: #CE0E2D;">Delivery Admin</p>
      </div>

      <!-- Error -->
      <div
        v-if="authStore.error"
        class="mb-4 rounded-lg bg-red-50 border border-red-200 px-4 py-2.5 text-xs text-red-600 font-medium"
      >
        {{ authStore.error }}
      </div>

      <!-- Form -->
      <form @submit.prevent="doLogin" class="space-y-4">
        <div>
          <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">
            Username
          </label>
          <input
            v-model="username"
            type="text"
            class="geo-input w-full"
            placeholder="admin"
          />
        </div>
        <div>
          <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">
            Password
          </label>
          <input
            v-model="password"
            type="password"
            class="geo-input w-full"
            placeholder="Enter password..."
            @keyup.enter="doLogin"
          />
        </div>
        <button
          type="submit"
          class="geo-btn-primary w-full rounded-lg py-2.5 text-sm font-bold"
          :disabled="loading"
        >
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>
    </div>
  </div>
</template>
