<script setup lang="ts">
import type { Member } from '@/types'
import {
  TrophyOutlined,
  SafetyCertificateOutlined,
  GlobalOutlined,
  HeartOutlined,
  CloseOutlined,
  LinkOutlined,
} from '@ant-design/icons-vue'
import { computed } from 'vue'

const props = defineProps<{ member: Member }>()
const emit = defineEmits<{ close: [] }>()

const statusClass: Record<string, string> = {
  active: 'geo-badge-green',
  expired: 'geo-badge-red',
  pending: 'geo-badge-yellow',
}

const langLevels: Record<string, number> = {
  'Native': 100, 'Fluent': 85, 'Professional': 70,
  'Intermediate': 50, 'Basic': 30, 'N/A': 0,
}

const avatarSrc = computed(() =>
  props.member.photo_url || `https://api.dicebear.com/7.x/bottts/svg?seed=${props.member.avatar_seed}`
)
</script>

<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center" style="background: rgba(15,19,30,0.6); backdrop-filter: blur(4px);" @click.self="emit('close')">
    <div class="geo-card w-full max-w-2xl max-h-[85vh] overflow-y-auto p-5 animate-slide-up">
      <!-- Header -->
      <div class="flex items-start justify-between mb-5">
        <div class="flex items-center gap-4">
          <!-- Gaming Avatar -->
          <div class="avatar-hex h-16 w-16 flex-shrink-0 overflow-hidden" style="background: linear-gradient(135deg, #FFF0F2, #FFD6DB);">
            <img :src="avatarSrc" class="h-full w-full object-cover" />
          </div>
          <div>
            <h2 class="text-lg font-extrabold tracking-tight" style="color: #1E2432;">{{ member.name }}</h2>
            <p class="text-xs font-semibold text-hw-gray-500">{{ member.title }}</p>
            <div class="mt-2 flex gap-1.5 flex-wrap">
              <span class="geo-badge text-[10px]">{{ member.team }}</span>
              <span class="geo-badge text-[10px]">{{ member.role }}</span>
              <span v-if="member.welink_id" class="geo-badge text-[10px] flex items-center gap-1">
                <LinkOutlined /> {{ member.welink_id }}
              </span>
            </div>
          </div>
        </div>
        <button class="rounded p-1.5 hover:bg-gray-100" style="color: #A1A8B5;" @click="emit('close')">
          <CloseOutlined />
        </button>
      </div>

      <p class="text-[13px] leading-relaxed mb-5 text-hw-gray-600">{{ member.bio }}</p>

      <!-- Skills -->
      <div class="mb-4">
        <div class="mb-1.5 flex items-center gap-1.5">
          <TrophyOutlined style="color: #CE0E2D; font-size: 13px;" />
          <h3 class="text-[10px] font-extrabold uppercase tracking-[0.1em] text-hw-gray-500">Skills</h3>
        </div>
        <div class="flex flex-wrap gap-1">
          <span v-for="s in member.skills" :key="s" class="geo-badge text-[10px]">{{ s }}</span>
        </div>
      </div>

      <!-- Certificates -->
      <div class="mb-4">
        <div class="mb-1.5 flex items-center gap-1.5">
          <SafetyCertificateOutlined style="color: #CE0E2D; font-size: 13px;" />
          <h3 class="text-[10px] font-extrabold uppercase tracking-[0.1em] text-hw-gray-500">Certificates</h3>
        </div>
        <div class="space-y-1">
          <div v-for="c in member.certificates" :key="c.name" class="flex items-center gap-2">
            <span :class="statusClass[c.status] || 'geo-badge'" class="text-[10px]">{{ c.name }}</span>
            <span v-if="c.issue_date" class="text-[10px] text-hw-gray-400">
              {{ c.issue_date }}{{ c.expiry_date ? ` → ${c.expiry_date}` : '' }}
            </span>
          </div>
        </div>
      </div>

      <!-- Languages -->
      <div class="mb-4">
        <div class="mb-1.5 flex items-center gap-1.5">
          <GlobalOutlined style="color: #CE0E2D; font-size: 13px;" />
          <h3 class="text-[10px] font-extrabold uppercase tracking-[0.1em] text-hw-gray-500">Languages</h3>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <div v-for="(level, lang) in member.languages" :key="lang" class="rounded p-2 border" style="border-color: #EEF0F4; background: #F7F8FA;">
            <p class="text-[9px] uppercase tracking-wider font-extrabold text-hw-gray-400">{{ lang }}</p>
            <p class="text-sm font-bold" style="color: #1E2432;">{{ level }}</p>
            <div class="mt-1 progress-bar-bg"><div class="progress-bar-fill" :style="{ width: `${langLevels[level] || 0}%` }"></div></div>
          </div>
        </div>
      </div>

      <!-- Fans -->
      <div>
        <div class="mb-1.5 flex items-center gap-1.5">
          <HeartOutlined style="color: #CE0E2D; font-size: 13px;" />
          <h3 class="text-[10px] font-extrabold uppercase tracking-[0.1em] text-hw-gray-500">Fans</h3>
          <span class="text-sm font-extrabold glow-text">{{ member.fans_count }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
