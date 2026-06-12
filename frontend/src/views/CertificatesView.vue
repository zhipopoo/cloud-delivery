<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useMemberStore } from '@/stores/members'
import {
  SafetyCertificateOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  CloseCircleOutlined,
} from '@ant-design/icons-vue'

const memberStore = useMemberStore()

onMounted(async () => {
  await memberStore.fetchMembers()
})

const statusIcon: Record<string, any> = {
  active: CheckCircleOutlined,
  expired: CloseCircleOutlined,
  pending: ClockCircleOutlined,
}

const statusClass: Record<string, string> = {
  active: 'geo-badge-green',
  expired: 'geo-badge-red',
  pending: 'geo-badge-yellow',
}

const techCerts = computed(() => {
  const items: { name: string; status: string; member: string; memberId: number }[] = []
  for (const m of memberStore.members) {
    for (const c of m.certificates) {
      if (c.category === 'technical') {
        items.push({ name: c.name, status: c.status, member: m.name, memberId: m.id })
      }
    }
  }
  return items
})

const generalCerts = computed(() => {
  const items: { name: string; status: string; member: string; memberId: number }[] = []
  for (const m of memberStore.members) {
    for (const c of m.certificates) {
      if (c.category === 'general') {
        items.push({ name: c.name, status: c.status, member: m.name, memberId: m.id })
      }
    }
  }
  return items
})
</script>

<template>
  <div class="space-y-6">
    <!-- Technical Certificates -->
    <div class="geo-card p-5 animate-slide-up">
      <div class="mb-4 flex items-center gap-3">
        <SafetyCertificateOutlined class="text-hw-blue" />
        <h2 class="text-sm font-bold uppercase tracking-wider text-gray-900">Technical Certificates</h2>
        <span class="geo-badge">{{ techCerts.length }}</span>
      </div>

      <div class="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="cert in techCerts"
          :key="`${cert.memberId}-${cert.name}`"
          class="flex items-center gap-3 rounded-lg border border-hw-red-100 bg-hw-gray-100 p-3 transition-all hover:border-hw-red-200"
        >
          <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-hw-red-50">
            <component :is="statusIcon[cert.status] || ClockCircleOutlined" class="text-lg" :class="cert.status === 'active' ? 'text-green-400' : cert.status === 'expired' ? 'text-red-400' : 'text-yellow-400'" />
          </div>
          <div class="min-w-0 flex-1">
            <p class="text-sm font-medium text-gray-900">{{ cert.name }}</p>
            <p class="text-xs text-hw-gray-600">{{ cert.member }}</p>
          </div>
          <span :class="statusClass[cert.status] || 'geo-badge'">{{ cert.status }}</span>
        </div>
      </div>
    </div>

    <!-- General Certificates -->
    <div class="geo-card p-5 animate-slide-up" style="animation-delay: 80ms">
      <div class="mb-4 flex items-center gap-3">
        <SafetyCertificateOutlined class="text-hw-red-500" />
        <h2 class="text-sm font-bold uppercase tracking-wider text-gray-900">General Certificates</h2>
        <span class="geo-badge">{{ generalCerts.length }}</span>
      </div>

      <div class="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="cert in generalCerts"
          :key="`${cert.memberId}-${cert.name}`"
          class="flex items-center gap-3 rounded-lg border border-hw-red-100 bg-hw-gray-100 p-3 transition-all hover:border-hw-red-200"
        >
          <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-hw-accent/10">
            <component :is="statusIcon[cert.status] || ClockCircleOutlined" class="text-lg" :class="cert.status === 'active' ? 'text-green-400' : cert.status === 'expired' ? 'text-red-400' : 'text-yellow-400'" />
          </div>
          <div class="min-w-0 flex-1">
            <p class="text-sm font-medium text-gray-900">{{ cert.name }}</p>
            <p class="text-xs text-hw-gray-600">{{ cert.member }}</p>
          </div>
          <span :class="statusClass[cert.status] || 'geo-badge'">{{ cert.status }}</span>
        </div>
      </div>
    </div>
  </div>
</template>