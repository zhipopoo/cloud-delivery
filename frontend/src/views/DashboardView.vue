<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useMemberStore } from '@/stores/members'
import { useProjectStore } from '@/stores/projects'
import {
  TeamOutlined,
  TrophyOutlined,
  SafetyCertificateOutlined,
  CalendarOutlined,
  HeartOutlined,
  RiseOutlined,
} from '@ant-design/icons-vue'

const memberStore = useMemberStore()
const projectStore = useProjectStore()

onMounted(async () => {
  await memberStore.fetchMembers()
  await projectStore.fetchProjects()
  await projectStore.fetchCalendar()
})

const totalMembers = computed(() => memberStore.members.length)
const totalProjects = computed(() => projectStore.projects.length)
const totalCerts = computed(() =>
  memberStore.members.reduce((sum, m) => sum + m.certificates.filter(c => c.status === 'active').length, 0)
)
const totalFans = computed(() => memberStore.members.reduce((sum, m) => sum + m.fans_count, 0))
const busyMembers = computed(() => projectStore.calendarData.filter(a => a.busy_level === 'red').length)
</script>

<template>
  <div class="space-y-6">
    <!-- Hero Stats -->
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <div class="geo-card-hover p-5 animate-slide-up" style="animation-delay: 0ms">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-xs font-medium uppercase tracking-wider text-hw-gray-600">Team Members</p>
            <p class="mt-2 text-3xl font-bold glow-text">{{ totalMembers }}</p>
          </div>
          <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-hw-red-50">
            <TeamOutlined class="text-xl text-hw-blue" />
          </div>
        </div>
        <div class="mt-3 flex items-center gap-1 text-xs text-hw-gray-600">
          <RiseOutlined class="text-green-400" />
          <span class="text-green-400">+3</span> this quarter
        </div>
      </div>

      <div class="geo-card-hover p-5 animate-slide-up" style="animation-delay: 80ms">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-xs font-medium uppercase tracking-wider text-hw-gray-600">Active Projects</p>
            <p class="mt-2 text-3xl font-bold glow-text">{{ totalProjects }}</p>
          </div>
          <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-hw-red-50">
            <CalendarOutlined class="text-xl text-hw-blue" />
          </div>
        </div>
        <div class="mt-3 flex items-center gap-1 text-xs text-hw-gray-600">
          <span class="h-2 w-2 rounded-full bg-red-500"></span>
          {{ busyMembers }} members at full capacity
        </div>
      </div>

      <div class="geo-card-hover p-5 animate-slide-up" style="animation-delay: 160ms">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-xs font-medium uppercase tracking-wider text-hw-gray-600">Active Certs</p>
            <p class="mt-2 text-3xl font-bold glow-text">{{ totalCerts }}</p>
          </div>
          <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-hw-red-50">
            <SafetyCertificateOutlined class="text-xl text-hw-blue" />
          </div>
        </div>
        <div class="mt-3 text-xs text-hw-gray-600">HCIE & Professional</div>
      </div>

      <div class="geo-card-hover p-5 animate-slide-up" style="animation-delay: 240ms">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-xs font-medium uppercase tracking-wider text-hw-gray-600">Total Fans</p>
            <p class="mt-2 text-3xl font-bold glow-text">{{ totalFans }}</p>
          </div>
          <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-hw-red-50">
            <HeartOutlined class="text-xl text-hw-blue" />
          </div>
        </div>
        <div class="mt-3 text-xs text-hw-gray-600">Peer recognition</div>
      </div>
    </div>

    <!-- Team Overview & Quick Calendar -->
    <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
      <!-- Team Members Grid -->
      <div class="geo-card col-span-1 p-5 lg:col-span-2">
        <h2 class="mb-4 text-sm font-semibold uppercase tracking-wider text-hw-gray-600">Team Overview</h2>
        <div class="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-3">
          <div
            v-for="m in memberStore.members"
            :key="m.id"
            class="group flex items-center gap-3 rounded-lg border border-hw-red-100 bg-hw-gray-100 p-3 transition-all hover:border-hw-red-200 hover:bg-gray-200/80"
          >
            <div class="avatar-hex h-10 w-10 flex-shrink-0 overflow-hidden bg-hw-red-50">
              <img
                :src="`https://api.dicebear.com/7.x/bottts/svg?seed=${m.avatar_seed}`"
                :alt="m.name"
                class="h-full w-full object-cover"
              />
            </div>
            <div class="min-w-0 flex-1">
              <p class="truncate text-sm font-semibold text-gray-900">{{ m.name }}</p>
              <p class="truncate text-xs text-hw-gray-600">{{ m.role }}</p>
            </div>
            <span class="geo-badge text-[10px]">{{ m.team }}</span>
          </div>
        </div>
      </div>

      <!-- Project Status -->
      <div class="geo-card p-5">
        <h2 class="mb-4 text-sm font-semibold uppercase tracking-wider text-hw-gray-600">Project Status</h2>
        <div class="space-y-3">
          <div
            v-for="p in projectStore.projects"
            :key="p.id"
            class="rounded-lg border border-hw-red-100 bg-hw-gray-100 p-3"
          >
            <div class="flex items-center justify-between">
              <p class="text-sm font-medium text-gray-900">{{ p.name }}</p>
              <span class="geo-badge-green text-[10px]">{{ p.status }}</span>
            </div>
            <p class="mt-1 text-xs text-hw-gray-600">{{ p.client }}</p>
            <div class="mt-2 progress-bar-bg">
              <div class="progress-bar-fill" :style="{ width: '65%' }"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>