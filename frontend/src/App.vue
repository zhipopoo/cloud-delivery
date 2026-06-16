<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMemberStore } from '@/stores/members'
import { useAuthStore } from '@/stores/auth'
import {
  DashboardOutlined,
  TeamOutlined,
  TrophyOutlined,
  SafetyCertificateOutlined,
  GlobalOutlined,
  HeartOutlined,
  CalendarOutlined,
  SettingOutlined,
  ProjectOutlined,
  UserOutlined,
  LogoutOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
} from '@ant-design/icons-vue'

const route = useRoute()
const router = useRouter()
const memberStore = useMemberStore()
const authStore = useAuthStore()
const collapsed = ref(false)

const isLoginPage = computed(() => route.path === '/login')
const isAdminPage = computed(() => route.path.startsWith('/admin'))

// ── Public nav items (no Admin link) ──
const publicNavItems = [
  { path: '/dashboard', label: 'Dashboard', icon: DashboardOutlined },
  { path: '/team', label: 'Team', icon: TeamOutlined },
  { path: '/skills', label: 'Skills', icon: TrophyOutlined },
  { path: '/certificates', label: 'Certificates', icon: SafetyCertificateOutlined },
  { path: '/languages', label: 'Languages', icon: GlobalOutlined },
  { path: '/calendar/personnel', label: 'Calendar', icon: CalendarOutlined },
  { path: '/fans', label: 'Fans', icon: HeartOutlined },
]

// ── Admin nav items ──
const adminNavItems = [
  { path: '/admin/members', label: 'Members', icon: TeamOutlined },
  { path: '/admin/projects', label: 'Projects', icon: ProjectOutlined },
  { path: '/admin/skills', label: 'Skills', icon: TrophyOutlined },
  { path: '/admin/certificates', label: 'Certificates', icon: SafetyCertificateOutlined },
  { path: '/admin/admins', label: 'Admins', icon: SettingOutlined },
]

function pageTitle(): string {
  if (isAdminPage.value) {
    return adminNavItems.find(i => route.path.startsWith(i.path))?.label || 'Admin'
  }
  return publicNavItems.find(i => route.path.startsWith(i.path))?.label || 'Portal'
}

function logout() {
  authStore.logout()
  router.push('/login')
}

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
  <!-- ═══════════ LOGIN: no sidebar/header ═══════════ -->
  <div v-if="isLoginPage" class="h-screen">
    <router-view />
  </div>

  <!-- ═══════════ NORMAL LAYOUT ═══════════ -->
  <div v-else class="flex h-screen overflow-hidden bg-[#F0F2F5]">
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
            <span v-if="isAdminPage" class="text-[9px] font-bold uppercase tracking-[0.12em]" style="color: #CE0E2D;">Admin Panel</span>
            <span v-else class="text-[9px] font-bold uppercase tracking-[0.12em]" style="color: #CE0E2D;">Delivery</span>
          </div>
        </transition>
      </div>

      <!-- ═══════════ PUBLIC SIDEBAR: Team Filter ═══════════ -->
      <template v-if="!isAdminPage">
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
      </template>

      <!-- ═══════════ ADMIN SIDEBAR: username info ═══════════ -->
      <template v-if="isAdminPage">
        <transition name="fade">
          <div v-if="!collapsed" class="px-3 py-2 border-b" style="border-color: #DDE1E8;">
            <div class="flex items-center gap-2">
              <UserOutlined style="color: #CE0E2D;" />
              <span class="text-[11px] font-semibold text-hw-gray-800">{{ authStore.username }}</span>
            </div>
          </div>
        </transition>
      </template>

      <!-- Nav -->
      <nav class="flex-1 overflow-y-auto px-2 py-2">
        <div class="space-y-0.5">
          <router-link
            v-for="item in (isAdminPage ? adminNavItems : publicNavItems)"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: route.path.startsWith(item.path) }"
          >
            <component :is="item.icon" class="text-base flex-shrink-0" />
            <transition name="fade">
              <span v-if="!collapsed" class="text-xs font-bold uppercase tracking-wide">{{ item.label }}</span>
            </transition>
          </router-link>
        </div>
      </nav>

      <!-- Footer -->
      <div class="border-t" style="border-color: #DDE1E8;">
        <!-- Admin Logout -->
        <button
          v-if="isAdminPage"
          class="flex w-full items-center justify-center gap-2 py-2.5 transition-colors hover:bg-red-50 text-hw-gray-500 hover:text-red-500"
          @click="logout"
        >
          <LogoutOutlined />
          <transition name="fade">
            <span v-if="!collapsed" class="text-xs font-bold uppercase tracking-wide">Logout</span>
          </transition>
        </button>

        <!-- Public Collapse toggle -->
        <button
          v-else
          class="flex items-center justify-center py-2.5 w-full transition-colors hover:bg-hw-red-50"
          style="color: #A1A8B5;"
          @click="collapsed = !collapsed"
        >
          <MenuUnfoldOutlined v-if="collapsed" />
          <MenuFoldOutlined v-else />
        </button>
      </div>
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
            {{ pageTitle() }}
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
