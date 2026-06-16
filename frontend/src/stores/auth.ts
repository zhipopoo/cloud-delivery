import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authApi } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('admin_token'))
  const username = ref<string>(localStorage.getItem('admin_username') || '')
  const error = ref('')

  function isAuthenticated(): boolean {
    return !!token.value
  }

  async function login(user: string, password: string): Promise<boolean> {
    error.value = ''
    try {
      const res = await authApi.login(user, password)
      token.value = res.data.token
      username.value = res.data.username
      localStorage.setItem('admin_token', res.data.token)
      localStorage.setItem('admin_username', res.data.username)
      return true
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Login failed'
      return false
    }
  }

  function logout() {
    token.value = null
    username.value = ''
    localStorage.removeItem('admin_token')
    localStorage.removeItem('admin_username')
  }

  return { token, username, error, isAuthenticated, login, logout }
})
