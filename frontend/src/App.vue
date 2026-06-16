<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useMemberStore } from '@/stores/members'
import {
  DashboardOutlined,
  TeamOutlined,
  TrophyOutlined,
  SafetyCertificateOutlined,
  GlobalOutlined,
  HeartOutlined,
  CalendarOutlined,
  SettingOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
} from '@ant-design/icons-vue'

const route = useRoute()
const memberStore = useMemberStore()
const collapsed = ref(false)

const navItems = [
  { path: '/dashboard', label: 'Dashboard', icon: DashboardOutlined },
  { path: '/team', label: 'Team', icon: TeamOutlined },
  { path: '/skills', label: 'Skills', icon: TrophyOutlined },
  { path: '/certificates', label: 'Certificates', icon: SafetyCertificateOutlined },
  { path: '/languages', label: 'Languages', icon: GlobalOutlined },
  { path: '/fans', label: 'Fans', icon: HeartOutlined },
  { path: '/calendar', label: 'Calendar', icon: CalendarOutlined },
  { path: '/admin', label: 'Admin', icon: SettingOutlined },
]

const currentTeam = ref<string | null>(null)
const teamTree = [
  { key: 'TMO', label: 'Technical TMO' },
  { key: 'PMO', label: 'Project Mgmt PMO' },
  { key: 'Management', label: 'Management' },
]

function onTeamSelect(key: string | null) {
  currentTeam.value = key
  memberStore.filterByTeam(key)
}
</script>

<template>
  <div class="flex h-screen overflow-hidden bg-[#F0F2F5]">
    <!-- ═══════════ SIDEBAR ═══════════ -->
    <aside
      class="relative z-10 flex flex-col transition-all duration-200 border-r bg-white"
      :class="collapsed ? 'w-14' : 'w-56'"
      style="border-color: #DDE1E8;"
    >
      <!-- Logo -->
      <div class="flex items-center gap-2 px-3 py-4 border-b" style="border-color: #DDE1E8;">
        <div class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded" style="background: #CE0E2D;">
          <svg class="h-4 w-4 text-white" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
        </div>
        <transition name="fade">
          <div v-if="!collapsed" class="flex flex-col leading-tight">
            <span class="text-[13px] font-extrabold tracking-tight" style="color: #1E2432;">HUAWEI CLOUD</span>
            <span class="text-[9px] font-bold uppercase tracking-[0.12em]" style="color: #CE0E2D;">Delivery</span>
          </div>
        </transition>
      </div>

      <!-- Team Filter -->
      <transition name="fade">
        <div v-if="!collapsed" class="px-3 py-2 border-b" style="border-color: #DDE1E8;">
          <div class="mb-1.5 text-[9px] font-extrabold uppercase tracking-[0.15em] text-hw-gray-500">Team</div>
          <div class="space-y-0.5">
            <button
              class="flex w-full items-center gap-2 rounded px-2 py-1 text-[11px] font-semibold transition-colors"
              :style="currentTeam === null
                ? 'background: #FFF0F2; color: #CE0E2D;'
                : 'color: #5E6573;'"
              @click="onTeamSelect(null)"
            >
              <span class="h-1.5 w-1.5 rounded-full" :style="{ background: currentTeam === null ? '#CE0E2D' : '#C5CAD5' }"></span>
              All Teams
            </button>
            <button
              v-for="t in teamTree" :key="t.key"
              class="flex w-full items-center gap-2 rounded px-2 py-1 text-[11px] font-semibold transition-colors"
              :style="currentTeam === t.key
                ? 'background: #FFF0F2; color: #CE0E2D;'
                : 'color: #5E6573;'"
              @click="onTeamSelect(t.key)"
            >
              <span class="h-1.5 w-1.5 rounded-full" :style="{ background: currentTeam === t.key ? '#CE0E2D' : '#C5CAD5' }"></span>
              {{ t.label }}
            </button>
          </div>
        </div>
      </transition>

      <!-- Nav -->
      <nav class="flex-1 overflow-y-auto px-2 py-2">
        <div class="space-y-0.5">
          <router-link
            v-for="item in navItems" :key="item.path" :to="item.path"
            class="nav-item"
            :class="{ active: route.path === item.path }"
          >
            <component :is="item.icon" class="text-base flex-shrink-0" />
            <transition name="fade">
              <span v-if="!collapsed" class="text-xs font-bold uppercase tracking-wide">{{ item.label }}</span>
            </transition>
          </router-link>
        </div>
      </nav>

      <!-- Collapse -->
      <button
        class="flex items-center justify-center py-2.5 border-t transition-colors hover:bg-hw-red-50"
        style="border-color: #DDE1E8; color: #A1A8B5;"
        @click="collapsed = !collapsed"
      >
        <MenuUnfoldOutlined v-if="collapsed" />
        <MenuFoldOutlined v-else />
      </button>
    </aside>

    <!-- ═══════════ MAIN ═══════════ -->
    <main class="relative z-10 flex-1 overflow-y-auto hex-grid">
      <!-- Top Bar -->
      <header
        class="sticky top-0 z-20 flex items-center justify-between px-5 py-2.5 border-b"
        style="background: rgba(255,255,255,0.92); backdrop-filter: blur(12px); border-color: #DDE1E8;"
      >
        <div class="flex items-center gap-3">
          <h1 class="text-base font-extrabold tracking-tight" style="color: #1E2432;">
            {{ navItems.find(i => i.path === route.path)?.label || 'Portal' }}
          </h1>
          <span class="geo-badge text-[10px]">v1.0</span>
        </div>
        <div class="flex items-center gap-2.5">
          <TeamOutlined style="color: #CE0E2D;" class="text-sm" />
          <span class="text-xs font-semibold text-hw-gray-500">Huawei Cloud Delivery</span>
        </div>
      </header>

      <!-- Page Content -->
      <div class="p-4">
        <router-view />
      </div>
    </main>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.15s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
