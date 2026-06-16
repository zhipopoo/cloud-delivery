<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { adminsApi } from '@/api'
import { useAuthStore } from '@/stores/auth'
import type { AdminUser } from '@/types'
import {
  PlusOutlined,
  DeleteOutlined,
  CloseOutlined,
} from '@ant-design/icons-vue'

const authStore = useAuthStore()
const admins = ref<AdminUser[]>([])
const showModal = ref(false)
const form = ref({ username: '', password: '' })
const formError = ref('')

onMounted(() => fetchAdmins())

async function fetchAdmins() {
  const res = await adminsApi.list()
  admins.value = res.data
}

function openNew() {
  form.value = { username: '', password: '' }
  formError.value = ''
  showModal.value = true
}

async function save() {
  formError.value = ''
  if (!form.value.username.trim() || !form.value.password.trim()) {
    formError.value = 'Both fields are required'
    return
  }
  if (form.value.password.length < 4) {
    formError.value = 'Password must be at least 4 characters'
    return
  }
  try {
    await adminsApi.create(form.value)
    showModal.value = false
    await fetchAdmins()
  } catch (e: any) {
    formError.value = e.response?.data?.detail || 'Failed to create user'
  }
}

async function remove(admin: AdminUser) {
  if (admin.username === authStore.username) {
    alert('Cannot delete yourself')
    return
  }
  if (!confirm(`Delete admin user "${admin.username}"?`)) return
  try {
    await adminsApi.delete(admin.id)
    await fetchAdmins()
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Failed to delete')
  }
}
</script>

<template>
  <div class="space-y-4 animate-slide-up">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h2 class="text-sm font-bold uppercase tracking-wider text-gray-900">
        Admin Users ({{ admins.length }})
      </h2>
      <button class="geo-btn-primary flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium" @click="openNew">
        <PlusOutlined /> Add Admin
      </button>
    </div>

    <!-- Table -->
    <div class="geo-card overflow-x-auto">
      <table class="w-full text-left text-xs">
        <thead>
          <tr class="border-b border-hw-red-100 text-hw-gray-600">
            <th class="whitespace-nowrap p-3 font-semibold uppercase tracking-wider">Username</th>
            <th class="whitespace-nowrap p-3 font-semibold uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="a in admins"
            :key="a.id"
            class="border-b border-gray-100 transition-colors hover:bg-hw-red-50/50"
          >
            <td class="p-3">
              <span class="font-medium text-gray-900">{{ a.username }}</span>
              <span v-if="a.username === authStore.username" class="ml-2 text-[10px] text-hw-gray-400">(you)</span>
            </td>
            <td class="p-3">
              <button
                class="rounded p-1.5 text-hw-gray-600 hover:bg-red-500/10 hover:text-red-400 transition-colors"
                :disabled="a.username === authStore.username"
                @click="remove(a)"
              >
                <DeleteOutlined />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
    >
      <div class="geo-card w-full max-w-md p-6 animate-slide-up">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-bold text-gray-900">New Admin User</h2>
          <button class="text-hw-gray-600 hover:text-gray-900" @click="showModal = false">
            <CloseOutlined class="text-lg" />
          </button>
        </div>

        <div v-if="formError" class="mb-4 rounded-lg bg-red-50 border border-red-200 px-3 py-2 text-xs text-red-600">
          {{ formError }}
        </div>

        <div class="space-y-4">
          <div>
            <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">Username *</label>
            <input v-model="form.username" class="geo-input w-full" placeholder="Username" @keyup.enter="save" />
          </div>
          <div>
            <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">Password *</label>
            <input v-model="form.password" type="password" class="geo-input w-full" placeholder="Min 4 characters" @keyup.enter="save" />
          </div>
        </div>

        <div class="flex items-center justify-end gap-3 mt-6 pt-4 border-t border-hw-red-100">
          <button class="rounded-lg px-4 py-2 text-sm text-hw-gray-600 hover:text-gray-900" @click="showModal = false">
            Cancel
          </button>
          <button class="geo-btn-primary rounded-lg px-6 py-2 text-sm font-medium" @click="save">
            Create
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
