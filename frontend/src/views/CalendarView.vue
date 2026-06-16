<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useProjectStore } from '@/stores/projects'
import { useMemberStore } from '@/stores/members'
import type { Assignment } from '@/types'
import { CalendarOutlined, TeamOutlined } from '@ant-design/icons-vue'

const projectStore = useProjectStore()
const memberStore = useMemberStore()
const selectedMemberId = ref<number | null>(null)
const selectedEvent = ref<Assignment | null>(null)
const currentYear = ref(2026)

onMounted(async () => {
  await projectStore.fetchCalendar()
  await projectStore.fetchProjects()
  await memberStore.fetchMembers()
})

const allMonths = computed(() => {
  const months: { label: string; idx: number }[] = []
  for (let m = 1; m <= 12; m++) {
    months.push({
      label: new Date(2026, m - 1).toLocaleString('en', { month: 'short', year: 'numeric' }),
      idx: m,
    })
  }
  return months
})

const membersWithAssignments = computed(() => {
  const map = new Map<number, Assignment[]>()
  for (const a of projectStore.calendarData) {
    const existing = map.get(a.member_id) || []
    existing.push(a)
    map.set(a.member_id, existing)
  }
  return memberStore.members
    .map(m => ({ member: m, assignments: map.get(m.id) || [] }))
    .filter(x => x.assignments.length > 0)
})

function getMonthIndex(dateStr: string): number {
  if (!dateStr) return 1
  const d = new Date(dateStr)
  if (isNaN(d.getTime())) return 1
  return d.getMonth() + 1
}

function getBarStyle(assignment: Assignment, monthIdx: number) {
  const startMonth = getMonthIndex(assignment.start)
  const endMonth = getMonthIndex(assignment.end)
  if (monthIdx < startMonth || monthIdx > endMonth) return null
  return {
    isFirst: monthIdx === startMonth,
    isLast: monthIdx === endMonth,
    label: monthIdx === startMonth ? `${assignment.project_name} · ${assignment.role_in_project || ''}` : '',
    color: assignment.busy_level,
    tooltip: `${assignment.member_name} — ${assignment.project_name}\n${assignment.role_in_project} | ${assignment.start} → ${assignment.end}`,
  }
}

const busyColors: Record<string, { bg: string }> = {
  red: { bg: 'bg-hw-red-600/20' },
  yellow: { bg: 'bg-hw-gold-400/30' },
  green: { bg: 'bg-green-100' },
}

const busyLabels: Record<string, string> = {
  red: 'Full Load', yellow: 'Moderate', green: 'Available',
}

function calcBarColor(a: Assignment, monthIdx: number): string {
  const style = getBarStyle(a, monthIdx)
  if (!style) return ''
  return busyColors[style.color]?.bg || ''
}

function onBarClick(a: Assignment) { selectedEvent.value = a }

function getEventAvatarUrl(): string {
  if (!selectedEvent.value) return ''
  const member = memberStore.members.find(m => m.id === selectedEvent.value!.member_id)
  if (!member) return ''
  return member.photo_url || `https://api.dicebear.com/7.x/bottts/svg?seed=${member.avatar_seed || 'default'}`
}

function getEventMemberTeam(): string {
  if (!selectedEvent.value) return ''
  return memberStore.members.find(m => m.id === selectedEvent.value!.member_id)?.team || ''
}

function prevYear() { currentYear.value-- }
function nextYear() { currentYear.value++ }

const filteredItems = computed(() => {
  if (!selectedMemberId.value) return membersWithAssignments.value
  return membersWithAssignments.value.filter(x => x.member.id === selectedMemberId.value)
})
</script>

<template>
  <div class="space-y-4">
    <!-- Timeline Header -->
    <div class="geo-card p-4 animate-slide-up">
      <div class="mb-3 flex items-center justify-between flex-wrap gap-2">
        <div class="flex items-center gap-2">
          <CalendarOutlined style="color: #CE0E2D;" />
          <h2 class="text-sm font-extrabold uppercase tracking-tight text-hw-gray-800">
            Personnel Project Timeline — {{ currentYear }}
          </h2>
        </div>
        <div class="flex items-center gap-2">
          <select v-model="selectedMemberId" class="geo-input text-xs" @change="selectedMemberId = selectedMemberId ? Number(selectedMemberId) : null">
            <option :value="null">All Members</option>
            <option v-for="m in memberStore.members" :key="m.id" :value="m.id">{{ m.name }}</option>
          </select>
          <div class="flex items-center gap-0.5">
            <button class="rounded px-2 py-1 text-xs font-bold text-hw-gray-500 hover:text-hw-red-600 hover:bg-hw-red-50" @click="prevYear">◀</button>
            <span class="text-sm font-extrabold text-hw-gray-800 min-w-[50px] text-center">{{ currentYear }}</span>
            <button class="rounded px-2 py-1 text-xs font-bold text-hw-gray-500 hover:text-hw-red-600 hover:bg-hw-red-50" @click="nextYear">▶</button>
          </div>
          <div class="flex items-center gap-2">
            <div class="flex items-center gap-1">
              <span class="h-2.5 w-6 rounded" style="background: #4CAF50;"></span>
              <span class="text-[10px] font-semibold text-hw-gray-500">Available</span>
            </div>
            <div class="flex items-center gap-1">
              <span class="h-2.5 w-6 rounded" style="background: #F5C842;"></span>
              <span class="text-[10px] font-semibold text-hw-gray-500">Moderate</span>
            </div>
            <div class="flex items-center gap-1">
              <span class="h-2.5 w-6 rounded" style="background: #CE0E2D;"></span>
              <span class="text-[10px] font-semibold text-hw-gray-500">Full Load</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Timeline Grid -->
      <div class="overflow-x-auto">
        <div class="min-w-[1200px]">
          <!-- Month Header -->
          <div class="mb-1 flex border-b pb-2" style="border-color: #DDE1E8;">
            <div class="w-52 flex-shrink-0 pr-4">
              <span class="text-[11px] font-extrabold uppercase tracking-wider text-hw-gray-500"><TeamOutlined class="mr-1" /> Member</span>
            </div>
            <div class="flex-1 grid grid-cols-12">
              <div v-for="month in allMonths" :key="month.idx" class="text-center text-[11px] font-extrabold uppercase tracking-wider text-hw-gray-500 border-l first:border-l-0" style="border-color: #DDE1E8;">
                {{ month.label }}
              </div>
            </div>
          </div>

          <!-- Member Rows -->
          <div class="space-y-px">
            <div v-for="{ member, assignments } in filteredItems" :key="member.id"
              class="flex items-stretch transition-colors border-b"
              style="border-color: #EEF0F4; background: #fff;">
              <!-- Member Info -->
              <div class="w-52 flex-shrink-0 flex items-center gap-2.5 p-2.5 border-r" style="border-color: #EEF0F4; background: #F7F8FA;">
                <div class="h-9 w-9 flex-shrink-0 rounded-full overflow-hidden border-2" style="border-color: #CE0E2D; box-shadow: 0 0 0 2px #fff, 0 0 8px rgba(206,14,45,0.25);">
                  <img :src="member.photo_url || `https://api.dicebear.com/7.x/bottts/svg?seed=${member.avatar_seed}`" class="h-full w-full object-cover" />
                </div>
                <div class="min-w-0">
                  <p class="text-sm font-extrabold text-hw-gray-800 truncate">{{ member.name }}</p>
                  <p class="text-[10px] font-semibold text-hw-gray-500 truncate">{{ member.team }} · {{ member.role }}</p>
                </div>
              </div>
              <!-- Month Cells - no gap, seamless -->
              <div class="flex-1 grid grid-cols-12 relative">
                <div v-for="month in allMonths" :key="month.idx" class="relative min-h-[72px] flex items-center border-l" style="border-color: #EEF0F4;">
                  <div v-for="a in assignments" :key="a.id">
                    <div v-if="getBarStyle(a, month.idx)"
                      class="absolute inset-x-0 cursor-pointer transition-all hover:brightness-110 flex items-center"
                      :style="{
                        top: `${(assignments.indexOf(a) % 4) * 16 + 3}px`,
                        height: '14px',
                        background: a.busy_level === 'red' ? '#CE0E2D' : a.busy_level === 'yellow' ? '#F5C842' : '#4CAF50',
                      }"
                      :title="a.project_name + ' — ' + a.role_in_project"
                      @click="onBarClick(a)">
                      <span v-if="getBarStyle(a, month.idx)?.label"
                        class="truncate px-1.5 text-[9px] font-extrabold text-white whitespace-nowrap"
                        style="text-shadow: 0 1px 2px rgba(0,0,0,0.5);">
                        {{ a.project_name }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="filteredItems.length === 0" class="py-12 text-center text-sm font-semibold text-hw-gray-400">
            No project assignments found.
          </div>
        </div>
      </div>
    </div>

    <!-- Detail Modal -->
    <div v-if="selectedEvent" class="fixed inset-0 z-50 flex items-center justify-center" style="background: rgba(15,19,30,0.6);" @click.self="selectedEvent = null">
      <div class="geo-card w-full max-w-md p-5 animate-slide-up">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-base font-extrabold text-hw-gray-800">Assignment Detail</h3>
          <button class="text-hw-gray-400 hover:text-hw-red-600 text-lg" @click="selectedEvent = null">✕</button>
        </div>
        <div v-if="selectedEvent" class="space-y-3">
          <div class="flex items-center gap-3">
            <div class="h-11 w-11 rounded-full overflow-hidden border-2" style="border-color: #CE0E2D; box-shadow: 0 0 0 2px #fff, 0 0 8px rgba(206,14,45,0.25);">
              <img :src="getEventAvatarUrl()" class="h-full w-full" />
            </div>
            <div>
              <p class="text-base font-extrabold text-hw-gray-800">{{ selectedEvent.member_name }}</p>
              <p class="text-xs font-semibold text-hw-gray-500">{{ getEventMemberTeam() }}</p>
            </div>
          </div>
          <div class="space-y-1.5">
            <div class="flex justify-between text-sm"><span class="text-hw-gray-500">Project</span><span class="font-bold text-hw-red-600">{{ selectedEvent.project_name }}</span></div>
            <div class="flex justify-between text-sm"><span class="text-hw-gray-500">Role</span><span class="font-bold text-hw-gray-800">{{ selectedEvent.role_in_project }}</span></div>
            <div class="flex justify-between text-sm"><span class="text-hw-gray-500">Period</span><span class="font-bold text-hw-gray-800">{{ selectedEvent.start }} → {{ selectedEvent.end }}</span></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
