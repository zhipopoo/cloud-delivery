<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { skillsApi } from '@/api'
import type { Skill } from '@/types'
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  CloseOutlined,
} from '@ant-design/icons-vue'

const skills = ref<Skill[]>([])
const showModal = ref(false)
const editingSkill = ref<Skill | null>(null)
const form = ref({ name: '', category: 'Cloud & Infra' })
const filterCategory = ref<string | null>(null)

const categories = [
  'Cloud & Infra',
  'Project & Process',
  'Security & Compliance',
  'Data & AI',
  'Business',
  'Other',
]

const filteredSkills = computed(() =>
  filterCategory.value
    ? skills.value.filter(s => s.category === filterCategory.value)
    : skills.value
)

onMounted(() => fetchSkills())

async function fetchSkills() {
  const res = await skillsApi.list()
  skills.value = res.data
}

function openNew() {
  editingSkill.value = null
  form.value = { name: '', category: 'Cloud & Infra' }
  showModal.value = true
}

function openEdit(s: Skill) {
  editingSkill.value = s
  form.value = { name: s.name, category: s.category }
  showModal.value = true
}

async function save() {
  if (!form.value.name.trim()) return
  if (editingSkill.value) {
    await skillsApi.update(editingSkill.value.id, form.value)
  } else {
    await skillsApi.create(form.value)
  }
  showModal.value = false
  await fetchSkills()
}

async function remove(id: number) {
  if (!confirm('Delete this skill?')) return
  await skillsApi.delete(id)
  await fetchSkills()
}
</script>

<template>
  <div class="space-y-4 animate-slide-up">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <h2 class="text-sm font-bold uppercase tracking-wider text-gray-900">
          Skills ({{ filteredSkills.length }})
        </h2>
        <select v-model="filterCategory" class="geo-input text-xs w-44">
          <option :value="null">All Categories</option>
          <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
        </select>
      </div>
      <button class="geo-btn-primary flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium" @click="openNew">
        <PlusOutlined /> Add Skill
      </button>
    </div>

    <!-- Table -->
    <div class="geo-card overflow-x-auto">
      <table class="w-full text-left text-xs">
        <thead>
          <tr class="border-b border-hw-red-100 text-hw-gray-600">
            <th class="whitespace-nowrap p-3 font-semibold uppercase tracking-wider">Name</th>
            <th class="whitespace-nowrap p-3 font-semibold uppercase tracking-wider">Category</th>
            <th class="whitespace-nowrap p-3 font-semibold uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="s in filteredSkills"
            :key="s.id"
            class="border-b border-gray-100 transition-colors hover:bg-hw-red-50/50"
          >
            <td class="p-3 font-medium text-gray-900">{{ s.name }}</td>
            <td class="p-3"><span class="geo-badge">{{ s.category }}</span></td>
            <td class="p-3">
              <div class="flex gap-1">
                <button class="rounded p-1.5 text-hw-gray-600 hover:bg-hw-red-50 hover:text-hw-red-600" @click="openEdit(s)">
                  <EditOutlined />
                </button>
                <button class="rounded p-1.5 text-hw-gray-600 hover:bg-red-500/10 hover:text-red-400" @click="remove(s.id)">
                  <DeleteOutlined />
                </button>
              </div>
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
          <h2 class="text-lg font-bold text-gray-900">
            {{ editingSkill ? 'Edit' : 'New' }} Skill
          </h2>
          <button class="text-hw-gray-600 hover:text-gray-900" @click="showModal = false">
            <CloseOutlined class="text-lg" />
          </button>
        </div>

        <div class="space-y-4">
          <div>
            <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">Name *</label>
            <input v-model="form.name" class="geo-input w-full" placeholder="Skill name" @keyup.enter="save" />
          </div>
          <div>
            <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">Category</label>
            <select v-model="form.category" class="geo-input w-full">
              <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
            </select>
          </div>
        </div>

        <div class="flex items-center justify-end gap-3 mt-6 pt-4 border-t border-hw-red-100">
          <button class="rounded-lg px-4 py-2 text-sm text-hw-gray-600 hover:text-gray-900" @click="showModal = false">
            Cancel
          </button>
          <button class="geo-btn-primary rounded-lg px-6 py-2 text-sm font-medium" @click="save">
            {{ editingSkill ? 'Update' : 'Create' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
