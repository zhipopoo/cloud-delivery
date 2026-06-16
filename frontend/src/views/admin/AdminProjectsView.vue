<script setup lang="ts">
import { onMounted, ref, reactive } from 'vue'
import { useMemberStore } from '@/stores/members'
import { useProjectStore } from '@/stores/projects'
import { projectsApi } from '@/api'
import type { Project, Assignment } from '@/types'
import {
  EditOutlined,
  DeleteOutlined,
  PlusOutlined,
  CloseOutlined,
  TeamOutlined,
} from '@ant-design/icons-vue'

const memberStore = useMemberStore()
const projectStore = useProjectStore()

const showProjectModal = ref(false)
const editingProject = ref<Project | null>(null)

const showAssignModal = ref(false)
const activeProject = ref<Project | null>(null)
const editingAssignment = ref<Assignment | null>(null)

const projectForm = reactive({
  name: '', client: '', description: '',
  start_date: '', end_date: '', status: 'active',
})

const assignForm = reactive({
  member_id: 0, project_id: 0,
  busy_level: 'green', role_in_project: '',
})

const busyLevels = [
  { value: 'green', label: 'Available', color: 'bg-green-500' },
  { value: 'yellow', label: 'Moderate Load', color: 'bg-yellow-500' },
  { value: 'red', label: 'Full Capacity', color: 'bg-red-500' },
]

onMounted(async () => {
  await projectStore.fetchProjects()
  await projectStore.fetchCalendar()
  await memberStore.fetchMembers()
})

// ── Project CRUD ──
function openNewProject() {
  editingProject.value = null
  Object.assign(projectForm, { name: '', client: '', description: '', start_date: '', end_date: '', status: 'active' })
  showProjectModal.value = true
}

function openEditProject(p: Project) {
  editingProject.value = p
  Object.assign(projectForm, { name: p.name, client: p.client, description: p.description, start_date: p.start_date, end_date: p.end_date, status: p.status })
  showProjectModal.value = true
}

async function saveProject() {
  if (editingProject.value) {
    await projectsApi.update(editingProject.value.id, projectForm)
  } else {
    await projectsApi.create(projectForm)
  }
  showProjectModal.value = false
  await projectStore.fetchProjects()
}

async function deleteProject(id: number) {
  if (!confirm('Delete this project? All related assignments will be removed.')) return
  await projectsApi.delete(id)
  await projectStore.fetchProjects()
  await projectStore.fetchCalendar()
}

// ── Assignment CRUD (per project) ──
function openManageTeam(p: Project) {
  activeProject.value = p
  editingAssignment.value = null
  Object.assign(assignForm, {
    member_id: memberStore.members[0]?.id || 0,
    project_id: p.id,
    busy_level: 'green',
    role_in_project: '',
  })
  showAssignModal.value = true
}

function projectAssignments(projectId: number): Assignment[] {
  return projectStore.calendarData.filter(a => a.project_id === projectId)
}

function openEditAssignment(a: Assignment) {
  editingAssignment.value = a
  Object.assign(assignForm, {
    member_id: a.member_id,
    project_id: a.project_id,
    busy_level: a.busy_level,
    role_in_project: a.role_in_project,
  })
}

async function saveAssignment() {
  if (editingAssignment.value) {
    await projectsApi.updateAssignment(editingAssignment.value.id, assignForm)
  } else {
    await projectsApi.assign(assignForm)
  }
  // reset to "add new" state
  editingAssignment.value = null
  Object.assign(assignForm, {
    member_id: memberStore.members[0]?.id || 0,
    project_id: activeProject.value!.id,
    busy_level: 'green',
    role_in_project: '',
  })
  await projectStore.fetchCalendar()
}

async function deleteAssignment(id: number) {
  if (!confirm('Remove this assignment?')) return
  await projectsApi.deleteAssignment(id)
  await projectStore.fetchCalendar()
}

function getMemberName(id: number) {
  return memberStore.members.find(m => m.id === id)?.name || '—'
}
</script>

<template>
  <div class="space-y-4 animate-slide-up">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h2 class="text-sm font-bold uppercase tracking-wider text-gray-900">
        Projects ({{ projectStore.projects.length }})
      </h2>
      <button class="geo-btn-primary flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium" @click="openNewProject">
        <PlusOutlined /> Add Project
      </button>
    </div>

    <!-- Project Cards -->
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="p in projectStore.projects"
        :key="p.id"
        class="geo-card p-4 transition-all hover:border-hw-red-200"
      >
        <div class="flex items-start justify-between mb-3">
          <div>
            <h3 class="text-sm font-bold text-gray-900">{{ p.name }}</h3>
            <p class="text-xs text-hw-gray-600">{{ p.client }}</p>
          </div>
          <span class="geo-badge" :class="p.status === 'active' ? 'geo-badge-green' : 'geo-badge-yellow'">{{ p.status }}</span>
        </div>
        <p class="text-xs text-hw-gray-600 mb-3 line-clamp-2">{{ p.description }}</p>
        <div class="flex items-center gap-2 text-[10px] text-hw-gray-600 mb-3">
          <span>{{ p.start_date }}</span>
          <span>→</span>
          <span>{{ p.end_date }}</span>
        </div>

        <!-- Assigned members summary -->
        <div class="mb-3">
          <div class="flex items-center gap-1 text-[10px] text-hw-gray-500 mb-1">
            <TeamOutlined /> Team ({{ projectAssignments(p.id).length }})
          </div>
          <div class="flex flex-wrap gap-1">
            <span
              v-for="a in projectAssignments(p.id)"
              :key="a.id"
              class="rounded px-1.5 py-0.5 text-[9px] font-medium"
              :class="a.busy_level === 'red' ? 'geo-badge-red' : a.busy_level === 'yellow' ? 'geo-badge-yellow' : 'geo-badge-green'"
            >
              {{ a.member_name }} · {{ a.role_in_project || 'Member' }}
            </span>
          </div>
        </div>

        <div class="flex gap-1">
          <button class="flex-1 rounded py-1.5 text-xs text-hw-gray-600 hover:bg-hw-red-50 hover:text-hw-blue transition-colors" @click="openEditProject(p)">
            <EditOutlined /> Edit
          </button>
          <button class="flex-1 rounded py-1.5 text-xs text-hw-gray-600 hover:bg-hw-red-50 hover:text-hw-red-600 transition-colors font-medium" @click="openManageTeam(p)">
            <TeamOutlined /> Manage Team
          </button>
          <button class="flex-1 rounded py-1.5 text-xs text-hw-gray-600 hover:bg-red-500/10 hover:text-red-400 transition-colors" @click="deleteProject(p.id)">
            <DeleteOutlined /> Delete
          </button>
        </div>
      </div>
    </div>

    <!-- ═══════════════ PROJECT EDIT MODAL ═══════════════ -->
    <div
      v-if="showProjectModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
    >
      <div class="geo-card w-full max-w-lg p-6 animate-slide-up">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-bold text-gray-900">
            {{ editingProject ? 'Edit' : 'New' }} Project
          </h2>
          <button class="text-hw-gray-600 hover:text-gray-900" @click="showProjectModal = false">
            <CloseOutlined class="text-lg" />
          </button>
        </div>

        <div class="space-y-4">
          <div>
            <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">Project Name *</label>
            <input v-model="projectForm.name" class="geo-input w-full" placeholder="Project name" />
          </div>
          <div>
            <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">Client</label>
            <input v-model="projectForm.client" class="geo-input w-full" placeholder="Client name" />
          </div>
          <div>
            <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">Description</label>
            <textarea v-model="projectForm.description" class="geo-input w-full h-20 resize-none" placeholder="Description..."></textarea>
          </div>
          <div class="grid grid-cols-3 gap-4">
            <div>
              <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">Start Date *</label>
              <input v-model="projectForm.start_date" type="date" class="geo-input w-full" />
            </div>
            <div>
              <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">End Date *</label>
              <input v-model="projectForm.end_date" type="date" class="geo-input w-full" />
            </div>
            <div>
              <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">Status</label>
              <select v-model="projectForm.status" class="geo-input w-full">
                <option value="active">Active</option>
                <option value="planning">Planning</option>
                <option value="completed">Completed</option>
              </select>
            </div>
          </div>
        </div>

        <div class="flex items-center justify-end gap-3 mt-6 pt-4 border-t border-hw-red-100">
          <button class="rounded-lg px-4 py-2 text-sm text-hw-gray-600 hover:text-gray-900" @click="showProjectModal = false">
            Cancel
          </button>
          <button class="geo-btn-primary rounded-lg px-6 py-2 text-sm font-medium" @click="saveProject">
            {{ editingProject ? 'Update' : 'Create' }} Project
          </button>
        </div>
      </div>
    </div>

    <!-- ═══════════════ TEAM MANAGEMENT MODAL ═══════════════ -->
    <div
      v-if="showAssignModal && activeProject"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
    >
      <div class="geo-card w-full max-w-2xl p-6 animate-slide-up max-h-[85vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h2 class="text-lg font-bold text-gray-900">Manage Team</h2>
            <p class="text-xs text-hw-gray-600">{{ activeProject.name }}</p>
          </div>
          <button class="text-hw-gray-600 hover:text-gray-900" @click="showAssignModal = false">
            <CloseOutlined class="text-lg" />
          </button>
        </div>

        <!-- Current assignments -->
        <div class="mb-6">
          <h3 class="text-xs font-semibold uppercase tracking-wider text-hw-gray-500 mb-2">
            Current Members ({{ projectAssignments(activeProject.id).length }})
          </h3>
          <div class="space-y-1.5">
            <div
              v-for="a in projectAssignments(activeProject.id)"
              :key="a.id"
              class="flex items-center justify-between rounded-lg border border-hw-red-100 bg-hw-gray-50 px-3 py-2"
            >
              <div class="flex items-center gap-3">
                <span class="text-sm font-medium text-gray-900">{{ a.member_name }}</span>
                <span class="text-xs text-hw-gray-600">{{ a.role_in_project || 'Member' }}</span>
                <span
                  class="rounded px-1.5 py-0.5 text-[10px] font-medium"
                  :class="a.busy_level === 'red' ? 'geo-badge-red' : a.busy_level === 'yellow' ? 'geo-badge-yellow' : 'geo-badge-green'"
                >{{ a.busy_level }}</span>
              </div>
              <div class="flex gap-1">
                <button class="rounded p-1 text-xs text-hw-gray-600 hover:text-hw-blue" @click="openEditAssignment(a)">Edit</button>
                <button class="rounded p-1 text-xs text-hw-gray-600 hover:text-red-400" @click="deleteAssignment(a.id)">Remove</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Add/Edit form -->
        <div class="border-t border-hw-red-100 pt-4">
          <h3 class="text-xs font-semibold uppercase tracking-wider text-hw-gray-500 mb-3">
            {{ editingAssignment ? 'Edit Assignment' : 'Add Member to Project' }}
          </h3>
          <div class="space-y-3">
            <div>
              <label class="block text-[10px] text-hw-gray-600 mb-1">Member</label>
              <select v-model="assignForm.member_id" class="geo-input w-full">
                <option v-for="m in memberStore.members" :key="m.id" :value="m.id">{{ m.name }} ({{ m.team }})</option>
              </select>
            </div>
            <div>
              <label class="block text-[10px] text-hw-gray-600 mb-1">Role in Project</label>
              <input v-model="assignForm.role_in_project" class="geo-input w-full" placeholder="e.g. Tech Lead, PM, TD" />
            </div>
            <div>
              <label class="block text-[10px] text-hw-gray-600 mb-1">Busy Level</label>
              <div class="flex gap-2">
                <button
                  v-for="bl in busyLevels"
                  :key="bl.value"
                  class="flex items-center gap-1.5 rounded-lg px-3 py-2 text-xs font-medium transition-all"
                  :class="assignForm.busy_level === bl.value
                    ? 'bg-hw-red-50 text-gray-900 border border-hw-blue'
                    : 'text-hw-gray-600 border border-transparent hover:border-hw-red-200'"
                  @click="assignForm.busy_level = bl.value"
                >
                  <span class="h-2.5 w-2.5 rounded-sm" :class="bl.color"></span>
                  {{ bl.label }}
                </button>
              </div>
            </div>
          </div>
          <div class="flex gap-2 mt-4">
            <button class="geo-btn-primary rounded-lg px-4 py-2 text-sm font-medium" @click="saveAssignment">
              {{ editingAssignment ? 'Update' : 'Add' }}
            </button>
            <button
              v-if="editingAssignment"
              class="rounded-lg px-4 py-2 text-sm text-hw-gray-600 hover:text-gray-900"
              @click="editingAssignment = null; Object.assign(assignForm, { member_id: memberStore.members[0]?.id || 0, project_id: activeProject?.id || 0, busy_level: 'green', role_in_project: '' })"
            >
              Cancel Edit
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
