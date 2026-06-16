<script setup lang="ts">
import { onMounted, ref, reactive, computed } from 'vue'
import { useMemberStore } from '@/stores/members'
import { useProjectStore } from '@/stores/projects'
import { membersApi, projectsApi, uploadsApi } from '@/api'
import type { Member, Project, Assignment, CertificateItem } from '@/types'
import {
  EditOutlined,
  DeleteOutlined,
  PlusOutlined,
  CloseOutlined,
  UploadOutlined,
  TeamOutlined,
  ProjectOutlined,
  ScheduleOutlined,
  SafetyCertificateOutlined,
} from '@ant-design/icons-vue'

const memberStore = useMemberStore()
const projectStore = useProjectStore()

const activeTab = ref<'members' | 'projects' | 'assignments'>('members')
const editingMember = ref<Member | null>(null)
const showMemberModal = ref(false)
const showProjectModal = ref(false)
const showAssignModal = ref(false)
const editingProject = ref<Project | null>(null)
const editingAssignment = ref<Assignment | null>(null)

// ── Member Form ──
const memberForm = reactive({
  name: '', avatar_seed: '', role: '', team: 'TMO',
  title: '', bio: '', welink_id: '', photo_url: '',
  skills: [] as string[],
  certificates: [] as CertificateItem[],
  languages: { cantonese: 'N/A', english: 'N/A', mandarin: 'N/A' },
  fans_count: 0,
})
const skillInput = ref('')

// ── Project Form ──
const projectForm = reactive({
  name: '', client: '', description: '',
  start_date: '', end_date: '', status: 'active',
})

// ── Assignment Form ──
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
  await memberStore.fetchMembers()
  await projectStore.fetchProjects()
  await projectStore.fetchCalendar()
})

// ── Member CRUD ──
function openNewMember() {
  editingMember.value = null
  Object.assign(memberForm, {
    name: '', avatar_seed: '', role: '', team: 'TMO',
    title: '', bio: '', welink_id: '', photo_url: '',
    skills: [], certificates: [],
    languages: { cantonese: 'N/A', english: 'N/A', mandarin: 'N/A' },
    fans_count: 0,
  })
  showMemberModal.value = true
}

function openEditMember(m: Member) {
  editingMember.value = m
  Object.assign(memberForm, {
    name: m.name, avatar_seed: m.avatar_seed,
    role: m.role, team: m.team,
    title: m.title, bio: m.bio,
    welink_id: m.welink_id || '', photo_url: m.photo_url || '',
    skills: [...m.skills],
    certificates: m.certificates.map(c => ({ ...c })),
    languages: { ...m.languages },
    fans_count: m.fans_count,
  })
  showMemberModal.value = true
}

async function saveMember() {
  const payload = {
    ...memberForm,
    skills: memberForm.skills,
    certificates: memberForm.certificates,
    avatar_seed: memberForm.avatar_seed || memberForm.name.toLowerCase().replace(/\s+/g, ''),
  }

  if (editingMember.value) {
    await membersApi.update(editingMember.value.id, payload)
  } else {
    await membersApi.create(payload)
  }
  showMemberModal.value = false
  await memberStore.fetchMembers()
}

async function deleteMember(id: number) {
  if (!confirm('Delete this member?')) return
  await membersApi.delete(id)
  await memberStore.fetchMembers()
}

// ── Skills ──
function addSkill() {
  const val = skillInput.value.trim()
  if (val && !memberForm.skills.includes(val)) {
    memberForm.skills.push(val)
  }
  skillInput.value = ''
}
function removeSkill(idx: number) { memberForm.skills.splice(idx, 1) }

// ── Certificates ──
function addCert() {
  memberForm.certificates.push({
    name: '', category: 'technical', status: 'active',
    issue_date: '', expiry_date: '', file_url: '',
  })
}
function removeCert(idx: number) { memberForm.certificates.splice(idx, 1) }
async function uploadCertFile(idx: number, e: Event) {
  const input = e.target as HTMLInputElement
  if (!input.files?.length) return
  const res = await uploadsApi.upload(input.files[0])
  memberForm.certificates[idx].file_url = res.data.url
}

// ── Photo upload ──
async function uploadPhoto(e: Event) {
  const input = e.target as HTMLInputElement
  if (!input.files?.length) return
  const res = await uploadsApi.upload(input.files[0])
  memberForm.photo_url = res.data.url
}

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

// ── Assignment CRUD ──
function openNewAssignment() {
  editingAssignment.value = null
  const [firstMember, firstProject] = [memberStore.members[0], projectStore.projects[0]]
  Object.assign(assignForm, {
    member_id: firstMember?.id || 0,
    project_id: firstProject?.id || 0,
    busy_level: 'green', role_in_project: '',
  })
  showAssignModal.value = true
}
function openEditAssignment(a: Assignment) {
  editingAssignment.value = a
  Object.assign(assignForm, {
    member_id: a.member_id, project_id: a.project_id,
    busy_level: a.busy_level, role_in_project: a.role_in_project,
  })
  showAssignModal.value = true
}
async function saveAssignment() {
  if (editingAssignment.value) {
    await projectsApi.updateAssignment(editingAssignment.value.id, assignForm)
  } else {
    await projectsApi.assign(assignForm)
  }
  showAssignModal.value = false
  await projectStore.fetchCalendar()
}
async function deleteAssignment(id: number) {
  if (!confirm('Delete this assignment?')) return
  await projectsApi.deleteAssignment(id)
  await projectStore.fetchCalendar()
}

function getMemberName(id: number) {
  return memberStore.members.find(m => m.id === id)?.name || '—'
}
function getProjectName(id: number) {
  return projectStore.projects.find(p => p.id === id)?.name || '—'
}

const langOptions: { key: 'cantonese' | 'english' | 'mandarin'; label: string }[] = [
  { key: 'cantonese', label: '粤语' },
  { key: 'english', label: 'English' },
  { key: 'mandarin', label: '普通话' },
]
</script>

<template>
  <div class="space-y-6">
    <!-- Tab Bar -->
    <div class="geo-card p-1 flex gap-1">
      <button
        v-for="tab in [
          { key: 'members', label: 'Members', icon: TeamOutlined },
          { key: 'projects', label: 'Projects', icon: ProjectOutlined },
          { key: 'assignments', label: 'Assignments', icon: ScheduleOutlined },
        ]"
        :key="tab.key"
        class="flex items-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium transition-all"
        :class="activeTab === tab.key
          ? 'bg-hw-blue text-gray-900 shadow-glow'
          : 'text-hw-gray-600 hover:text-gray-900 hover:bg-gray-200'"
        @click="activeTab = tab.key as any"
      >
        <component :is="tab.icon" />
        {{ tab.label }}
      </button>
    </div>

    <!-- ═══════════════ MEMBERS TAB ═══════════════ -->
    <div v-if="activeTab === 'members'" class="space-y-4 animate-slide-up">
      <div class="flex items-center justify-between">
        <h2 class="text-sm font-bold uppercase tracking-wider text-gray-900">
          Member Directory ({{ memberStore.members.length }})
        </h2>
        <button class="geo-btn-primary flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium" @click="openNewMember">
          <PlusOutlined /> Add Member
        </button>
      </div>

      <!-- Members Table -->
      <div class="geo-card overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead>
            <tr class="border-b border-hw-red-100 text-hw-gray-600">
              <th class="whitespace-nowrap p-3 font-semibold uppercase tracking-wider">Photo</th>
              <th class="whitespace-nowrap p-3 font-semibold uppercase tracking-wider">Name</th>
              <th class="whitespace-nowrap p-3 font-semibold uppercase tracking-wider">Team</th>
              <th class="whitespace-nowrap p-3 font-semibold uppercase tracking-wider">Role</th>
              <th class="whitespace-nowrap p-3 font-semibold uppercase tracking-wider">WeLink ID</th>
              <th class="whitespace-nowrap p-3 font-semibold uppercase tracking-wider">Title</th>
              <th class="whitespace-nowrap p-3 font-semibold uppercase tracking-wider">Certs</th>
              <th class="whitespace-nowrap p-3 font-semibold uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="m in memberStore.members"
              :key="m.id"
              class="border-b border-gray-100 transition-colors hover:bg-hw-red-50/50"
            >
              <td class="p-3">
                <div class="avatar-hex h-10 w-10 overflow-hidden">
                  <img
                    :src="m.photo_url || `https://api.dicebear.com/7.x/bottts/svg?seed=${m.avatar_seed}`"
                    class="h-full w-full object-cover"
                  />
                </div>
              </td>
              <td class="p-3 font-medium text-gray-900">{{ m.name }}</td>
              <td class="p-3"><span class="geo-badge">{{ m.team }}</span></td>
              <td class="p-3 text-hw-gray-600">{{ m.role }}</td>
              <td class="p-3 font-mono text-hw-red-500">{{ m.welink_id || '—' }}</td>
              <td class="p-3 text-hw-gray-600 max-w-[200px] truncate">{{ m.title }}</td>
              <td class="p-3">
                <div class="flex gap-1">
                  <span
                    v-for="c in m.certificates"
                    :key="c.name"
                    class="rounded px-1.5 py-0.5 text-[10px]"
                    :class="c.status === 'active' ? 'geo-badge-green' : c.status === 'expired' ? 'geo-badge-red' : 'geo-badge-yellow'"
                  >{{ c.name }}</span>
                </div>
              </td>
              <td class="p-3">
                <div class="flex gap-1">
                  <button class="rounded p-1.5 text-hw-gray-600 hover:bg-hw-red-50 hover:text-hw-red-600 transition-colors" title="Edit" @click="openEditMember(m)">
                    <EditOutlined />
                  </button>
                  <button class="rounded p-1.5 text-hw-gray-600 hover:bg-red-500/10 hover:text-red-400 transition-colors" title="Delete" @click="deleteMember(m.id)">
                    <DeleteOutlined />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ═══════════════ PROJECTS TAB ═══════════════ -->
    <div v-if="activeTab === 'projects'" class="space-y-4 animate-slide-up">
      <div class="flex items-center justify-between">
        <h2 class="text-sm font-bold uppercase tracking-wider text-gray-900">
          Projects ({{ projectStore.projects.length }})
        </h2>
        <button class="geo-btn-primary flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium" @click="openNewProject">
          <PlusOutlined /> Add Project
        </button>
      </div>

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
          <div class="flex gap-1">
            <button class="flex-1 rounded py-1.5 text-xs text-hw-gray-600 hover:bg-hw-red-50 hover:text-hw-red-600 transition-colors" @click="openEditProject(p)">
              <EditOutlined /> Edit
            </button>
            <button class="flex-1 rounded py-1.5 text-xs text-hw-gray-600 hover:bg-red-500/10 hover:text-red-400 transition-colors" @click="deleteProject(p.id)">
              <DeleteOutlined /> Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══════════════ ASSIGNMENTS TAB ═══════════════ -->
    <div v-if="activeTab === 'assignments'" class="space-y-4 animate-slide-up">
      <div class="flex items-center justify-between">
        <h2 class="text-sm font-bold uppercase tracking-wider text-gray-900">
          Resource Assignments ({{ projectStore.calendarData.length }})
        </h2>
        <button class="geo-btn-primary flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium" @click="openNewAssignment">
          <PlusOutlined /> New Assignment
        </button>
      </div>

      <div class="geo-card overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead>
            <tr class="border-b border-hw-red-100 text-hw-gray-600">
              <th class="whitespace-nowrap p-3 font-semibold uppercase tracking-wider">Member</th>
              <th class="whitespace-nowrap p-3 font-semibold uppercase tracking-wider">Project</th>
              <th class="whitespace-nowrap p-3 font-semibold uppercase tracking-wider">Role</th>
              <th class="whitespace-nowrap p-3 font-semibold uppercase tracking-wider">Busy Level</th>
              <th class="whitespace-nowrap p-3 font-semibold uppercase tracking-wider">Period</th>
              <th class="whitespace-nowrap p-3 font-semibold uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="a in projectStore.calendarData"
              :key="a.id"
              class="border-b border-gray-100 transition-colors hover:bg-hw-red-50/50"
            >
              <td class="p-3 font-medium text-gray-900">{{ a.member_name }}</td>
              <td class="p-3 text-hw-gray-600">{{ a.project_name }}</td>
              <td class="p-3 text-hw-gray-600">{{ a.role_in_project }}</td>
              <td class="p-3">
                <span class="rounded px-2 py-0.5 text-[10px] font-medium"
                  :class="a.busy_level === 'red' ? 'geo-badge-red' : a.busy_level === 'yellow' ? 'geo-badge-yellow' : 'geo-badge-green'"
                >{{ a.busy_level }}</span>
              </td>
              <td class="p-3 text-hw-gray-600">{{ a.start }} → {{ a.end }}</td>
              <td class="p-3">
                <div class="flex gap-1">
                  <button class="rounded p-1.5 text-hw-gray-600 hover:bg-hw-red-50 hover:text-hw-blue" @click="openEditAssignment(a)">
                    <EditOutlined />
                  </button>
                  <button class="rounded p-1.5 text-hw-gray-600 hover:bg-red-500/10 hover:text-red-400" @click="deleteAssignment(a.id)">
                    <DeleteOutlined />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ═══════════════ MEMBER EDIT MODAL ═══════════════ -->
    <div
      v-if="showMemberModal"
      class="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-black/60 backdrop-blur-sm py-8"
    >
      <div class="geo-card w-full max-w-3xl p-6 animate-slide-up">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-bold text-gray-900">
            {{ editingMember ? 'Edit' : 'New' }} Member
          </h2>
          <button class="text-hw-gray-600 hover:text-gray-900" @click="showMemberModal = false">
            <CloseOutlined class="text-lg" />
          </button>
        </div>

        <div class="space-y-5 max-h-[70vh] overflow-y-auto pr-2">
          <!-- Row 1: Basic Info -->
          <div class="grid grid-cols-3 gap-4">
            <div>
              <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">Name *</label>
              <input v-model="memberForm.name" class="geo-input w-full" placeholder="Full name" />
            </div>
            <div>
              <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">Team *</label>
              <select v-model="memberForm.team" class="geo-input w-full">
                <option value="TMO">TMO</option>
                <option value="PMO">PMO</option>
                <option value="Management">Management</option>
              </select>
            </div>
            <div>
              <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">Role *</label>
              <input v-model="memberForm.role" class="geo-input w-full" placeholder="e.g. TMO Lead" />
            </div>
          </div>

          <!-- Row 2: Title / WeLink / Avatar Seed -->
          <div class="grid grid-cols-3 gap-4">
            <div>
              <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">Title</label>
              <input v-model="memberForm.title" class="geo-input w-full" placeholder="e.g. Senior Architect" />
            </div>
            <div>
              <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">
                <span class="text-hw-red-500">WeLink ID</span>
              </label>
              <input v-model="memberForm.welink_id" class="geo-input w-full font-mono" placeholder="e.g. zhangsan001" />
            </div>
            <div>
              <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">Avatar Seed</label>
              <input v-model="memberForm.avatar_seed" class="geo-input w-full" placeholder="DiceBear seed" />
            </div>
          </div>

          <!-- Row 3: Bio -->
          <div>
            <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">Bio</label>
            <textarea v-model="memberForm.bio" class="geo-input w-full h-20 resize-none" placeholder="Short biography..."></textarea>
          </div>

          <!-- Row 4: Photo Upload -->
          <div class="flex items-center gap-4">
            <div>
              <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-2">Profile Photo</label>
              <div class="flex items-center gap-3">
                <div class="avatar-hex h-16 w-16 overflow-hidden bg-hw-red-50">
                  <img
                    :src="memberForm.photo_url || `https://api.dicebear.com/7.x/bottts/svg?seed=${memberForm.avatar_seed || 'default'}`"
                    class="h-full w-full object-cover"
                  />
                </div>
                <label class="geo-btn-primary cursor-pointer rounded-lg px-3 py-1.5 text-xs font-medium">
                  <UploadOutlined /> Upload Photo
                  <input type="file" accept="image/*" class="hidden" @change="uploadPhoto" />
                </label>
                <button
                  v-if="memberForm.photo_url"
                  class="text-xs text-hw-gray-600 hover:text-red-400"
                  @click="memberForm.photo_url = ''"
                >Clear</button>
              </div>
            </div>
          </div>

          <!-- Row 5: Skills -->
          <div>
            <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-2">Skills</label>
            <div class="flex flex-wrap gap-1.5 mb-2">
              <span
                v-for="(s, idx) in memberForm.skills"
                :key="idx"
                class="geo-badge flex items-center gap-1 cursor-pointer"
                @click="removeSkill(idx)"
              >
                {{ s }} ✕
              </span>
            </div>
            <div class="flex gap-2">
              <input
                v-model="skillInput"
                class="geo-input flex-1"
                placeholder="Add skill..."
                @keyup.enter="addSkill"
              />
              <button class="geo-btn-primary rounded-lg px-3 py-1.5 text-xs" @click="addSkill">+ Add</button>
            </div>
          </div>

          <!-- Row 6: Languages -->
          <div>
            <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-2">Languages</label>
            <div class="grid grid-cols-3 gap-3">
              <div v-for="opt in langOptions" :key="opt.key">
                <label class="text-[10px] text-hw-gray-600 mb-1 block">{{ opt.label }}</label>
                <select v-model="memberForm.languages[opt.key]" class="geo-input w-full">
                  <option value="Native">Native</option>
                  <option value="Fluent">Fluent</option>
                  <option value="Professional">Professional</option>
                  <option value="Intermediate">Intermediate</option>
                  <option value="Basic">Basic</option>
                  <option value="N/A">N/A</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Row 7: Certificates -->
          <div>
            <div class="flex items-center justify-between mb-2">
              <label class="text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600">
                <SafetyCertificateOutlined class="mr-1" /> Certificates
              </label>
              <button class="geo-btn-primary rounded-lg px-3 py-1 text-xs" @click="addCert">+ Add Cert</button>
            </div>

            <div v-if="memberForm.certificates.length === 0" class="text-xs text-hw-gray-600 py-2">
              No certificates. Click "+ Add Cert" to add one.
            </div>

            <div
              v-for="(cert, idx) in memberForm.certificates"
              :key="idx"
              class="rounded-lg border border-hw-red-100 bg-hw-gray-50 p-3 mb-2"
            >
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-semibold text-hw-gray-600">Certificate #{{ idx + 1 }}</span>
                <button class="text-xs text-red-400 hover:text-red-300" @click="removeCert(idx)">Remove</button>
              </div>
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="text-[10px] text-hw-gray-600">Name *</label>
                  <input v-model="cert.name" class="geo-input w-full" placeholder="e.g. HCIE-Cloud" />
                </div>
                <div>
                  <label class="text-[10px] text-hw-gray-600">Category</label>
                  <select v-model="cert.category" class="geo-input w-full">
                    <option value="technical">Technical</option>
                    <option value="general">General</option>
                  </select>
                </div>
              </div>
              <div class="grid grid-cols-3 gap-3 mt-2">
                <div>
                  <label class="text-[10px] text-hw-gray-600">Status</label>
                  <select v-model="cert.status" class="geo-input w-full">
                    <option value="active">Active</option>
                    <option value="expired">Expired</option>
                    <option value="pending">Pending</option>
                  </select>
                </div>
                <div>
                  <label class="text-[10px] text-hw-gray-600">Issue Date</label>
                  <input v-model="cert.issue_date" type="date" class="geo-input w-full" />
                </div>
                <div>
                  <label class="text-[10px] text-hw-gray-600">Expiry Date</label>
                  <input v-model="cert.expiry_date" type="date" class="geo-input w-full" />
                </div>
              </div>
              <div class="flex items-center gap-3 mt-2">
                <label class="geo-btn-primary cursor-pointer rounded px-2 py-1 text-[10px]">
                  <UploadOutlined /> Upload Cert File
                  <input type="file" accept=".pdf,.jpg,.png,.doc,.docx" class="hidden" @change="uploadCertFile(idx, $event)" />
                </label>
                <span v-if="cert.file_url" class="text-[10px] text-green-400">✓ File uploaded</span>
                <span v-else class="text-[10px] text-hw-gray-600">No file</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="flex items-center justify-end gap-3 mt-6 pt-4 border-t border-hw-red-100">
          <button class="rounded-lg px-4 py-2 text-sm text-hw-gray-600 hover:text-gray-900" @click="showMemberModal = false">
            Cancel
          </button>
          <button class="geo-btn-primary rounded-lg px-6 py-2 text-sm font-medium" @click="saveMember">
            {{ editingMember ? 'Update' : 'Create' }} Member
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

    <!-- ═══════════════ ASSIGNMENT EDIT MODAL ═══════════════ -->
    <div
      v-if="showAssignModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
    >
      <div class="geo-card w-full max-w-md p-6 animate-slide-up">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-bold text-gray-900">
            {{ editingAssignment ? 'Edit' : 'New' }} Assignment
          </h2>
          <button class="text-hw-gray-600 hover:text-gray-900" @click="showAssignModal = false">
            <CloseOutlined class="text-lg" />
          </button>
        </div>

        <div class="space-y-4">
          <div>
            <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">Member</label>
            <select v-model="assignForm.member_id" class="geo-input w-full">
              <option v-for="m in memberStore.members" :key="m.id" :value="m.id">{{ m.name }} ({{ m.team }})</option>
            </select>
          </div>
          <div>
            <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">Project</label>
            <select v-model="assignForm.project_id" class="geo-input w-full">
              <option v-for="p in projectStore.projects" :key="p.id" :value="p.id">{{ p.name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">Role in Project</label>
            <input v-model="assignForm.role_in_project" class="geo-input w-full" placeholder="e.g. Tech Lead" />
          </div>
          <div>
            <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-2">Busy Level</label>
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

        <div class="flex items-center justify-end gap-3 mt-6 pt-4 border-t border-hw-red-100">
          <button class="rounded-lg px-4 py-2 text-sm text-hw-gray-600 hover:text-gray-900" @click="showAssignModal = false">
            Cancel
          </button>
          <button class="geo-btn-primary rounded-lg px-6 py-2 text-sm font-medium" @click="saveAssignment">
            {{ editingAssignment ? 'Update' : 'Create' }} Assignment
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
