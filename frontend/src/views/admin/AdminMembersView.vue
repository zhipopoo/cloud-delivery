<script setup lang="ts">
import { onMounted, ref, reactive } from 'vue'
import { useMemberStore } from '@/stores/members'
import { membersApi, uploadsApi, skillsApi, certTemplatesApi } from '@/api'
import type { Member, CertificateItem, Skill, CertificateTemplate } from '@/types'
import {
  EditOutlined,
  DeleteOutlined,
  PlusOutlined,
  CloseOutlined,
  UploadOutlined,
  SafetyCertificateOutlined,
} from '@ant-design/icons-vue'

const memberStore = useMemberStore()
const editingMember = ref<Member | null>(null)
const showModal = ref(false)
const skillInput = ref('')

// Managed skill & cert lists for autocomplete
const managedSkills = ref<Skill[]>([])
const managedCerts = ref<CertificateTemplate[]>([])

const memberForm = reactive({
  name: '', avatar_seed: '', role: '', team: 'TMO',
  title: '', bio: '', welink_id: '', photo_url: '',
  skills: [] as string[],
  certificates: [] as CertificateItem[],
  languages: { cantonese: 'N/A', english: 'N/A', mandarin: 'N/A' },
  fans_count: 0,
})

const langOptions: { key: 'cantonese' | 'english' | 'mandarin'; label: string }[] = [
  { key: 'cantonese', label: '粤语' },
  { key: 'english', label: 'English' },
  { key: 'mandarin', label: '普通话' },
]

onMounted(async () => {
  await memberStore.fetchMembers()
  try {
    const [sk, ct] = await Promise.all([skillsApi.list(), certTemplatesApi.list()])
    managedSkills.value = sk.data
    managedCerts.value = ct.data
  } catch (_) { /* API might not be available yet */ }
})

// ── Member CRUD ──
function openNew() {
  editingMember.value = null
  Object.assign(memberForm, {
    name: '', avatar_seed: '', role: '', team: 'TMO',
    title: '', bio: '', welink_id: '', photo_url: '',
    skills: [], certificates: [],
    languages: { cantonese: 'N/A', english: 'N/A', mandarin: 'N/A' },
    fans_count: 0,
  })
  showModal.value = true
}

function openEdit(m: Member) {
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
  showModal.value = true
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
  showModal.value = false
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

// skill autocomplete suggestions (not yet selected)
function skillSuggestions(): Skill[] {
  if (!skillInput.value) return []
  return managedSkills.value.filter(
    s => !memberForm.skills.includes(s.name) && s.name.toLowerCase().includes(skillInput.value.toLowerCase())
  ).slice(0, 6)
}

function selectSkill(name: string) {
  if (!memberForm.skills.includes(name)) {
    memberForm.skills.push(name)
  }
  skillInput.value = ''
}

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

// ── Photo ──
async function uploadPhoto(e: Event) {
  const input = e.target as HTMLInputElement
  if (!input.files?.length) return
  const res = await uploadsApi.upload(input.files[0])
  memberForm.photo_url = res.data.url
}

function certNameSuggestions(idx: number): CertificateTemplate[] {
  const q = memberForm.certificates[idx].name.toLowerCase()
  if (!q) return managedCerts.value.slice(0, 6)
  return managedCerts.value.filter(t => t.name.toLowerCase().includes(q)).slice(0, 6)
}
</script>

<template>
  <div class="space-y-4 animate-slide-up">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h2 class="text-sm font-bold uppercase tracking-wider text-gray-900">
        Member Directory ({{ memberStore.members.length }})
      </h2>
      <button class="geo-btn-primary flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium" @click="openNew">
        <PlusOutlined /> Add Member
      </button>
    </div>

    <!-- Table -->
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
                <button class="rounded p-1.5 text-hw-gray-600 hover:bg-hw-red-50 hover:text-hw-red-600" @click="openEdit(m)">
                  <EditOutlined />
                </button>
                <button class="rounded p-1.5 text-hw-gray-600 hover:bg-red-500/10 hover:text-red-400" @click="deleteMember(m.id)">
                  <DeleteOutlined />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ═══════════════ MEMBER EDIT MODAL ═══════════════ -->
    <div
      v-if="showModal"
      class="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-black/60 backdrop-blur-sm py-8"
    >
      <div class="geo-card w-full max-w-3xl p-6 animate-slide-up">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-bold text-gray-900">
            {{ editingMember ? 'Edit' : 'New' }} Member
          </h2>
          <button class="text-hw-gray-600 hover:text-gray-900" @click="showModal = false">
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
              <label class="block text-[10px] font-semibold uppercase tracking-wider text-hw-gray-600 mb-1">WeLink ID</label>
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

          <!-- Row 4: Photo -->
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
            <div class="flex gap-2 relative">
              <input
                v-model="skillInput"
                class="geo-input flex-1"
                placeholder="Add skill..."
                @keyup.enter="addSkill"
              />
              <button class="geo-btn-primary rounded-lg px-3 py-1.5 text-xs" @click="addSkill">+ Add</button>
              <!-- Autocomplete dropdown -->
              <div
                v-if="skillSuggestions().length"
                class="absolute top-full left-0 right-0 mt-1 rounded-lg border border-hw-red-100 bg-white shadow-lg z-10"
              >
                <div
                  v-for="s in skillSuggestions()"
                  :key="s.id"
                  class="px-3 py-1.5 text-xs hover:bg-hw-red-50 cursor-pointer flex justify-between"
                  @click="selectSkill(s.name)"
                >
                  <span>{{ s.name }}</span>
                  <span class="text-hw-gray-400">{{ s.category }}</span>
                </div>
              </div>
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
              No certificates.
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
              <div class="grid grid-cols-2 gap-3 relative">
                <div class="relative">
                  <label class="text-[10px] text-hw-gray-600">Name *</label>
                  <input v-model="cert.name" class="geo-input w-full" placeholder="e.g. HCIE-Cloud" />
                  <div
                    v-if="certNameSuggestions(idx).length"
                    class="absolute top-full left-0 right-0 mt-1 rounded-lg border border-hw-red-100 bg-white shadow-lg z-10"
                  >
                    <div
                      v-for="t in certNameSuggestions(idx)"
                      :key="t.id"
                      class="px-3 py-1.5 text-xs hover:bg-hw-red-50 cursor-pointer"
                      @click="cert.name = t.name; cert.category = t.category"
                    >
                      {{ t.name }} <span class="text-hw-gray-400">({{ t.category }})</span>
                    </div>
                  </div>
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

        <div class="flex items-center justify-end gap-3 mt-6 pt-4 border-t border-hw-red-100">
          <button class="rounded-lg px-4 py-2 text-sm text-hw-gray-600 hover:text-gray-900" @click="showModal = false">
            Cancel
          </button>
          <button class="geo-btn-primary rounded-lg px-6 py-2 text-sm font-medium" @click="saveMember">
            {{ editingMember ? 'Update' : 'Create' }} Member
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
