<script setup lang="ts">
import { onMounted } from 'vue'
import { useMemberStore } from '@/stores/members'

const memberStore = useMemberStore()

onMounted(async () => {
  await memberStore.fetchMembers()
})

const langLevels: Record<string, number> = {
  'Native': 100, 'Fluent': 85, 'Professional': 70,
  'Intermediate': 50, 'Basic': 30, 'N/A': 0,
}

const langBarColors: Record<string, string> = {
  'Native': '#CE0E2D',
  'Fluent': '#E6002D',
  'Professional': '#FF5C72',
  'Intermediate': '#F5C842',
  'Basic': '#D4A830',
  'N/A': '#C5CAD5',
}

const languages = ['cantonese', 'english', 'mandarin'] as const
const langLabels: Record<string, string> = {
  cantonese: 'Cantonese', english: 'English', mandarin: 'Mandarin',
}
</script>

<template>
  <div class="space-y-5">
    <!-- Language Matrix -->
    <div class="geo-card p-4 animate-slide-up">
      <h2 class="mb-4 text-sm font-extrabold uppercase tracking-wider text-hw-gray-800">Language Proficiency Matrix</h2>

      <!-- Matrix Header -->
      <div class="mb-2 grid grid-cols-4 gap-3 px-2">
        <div class="text-[11px] font-extrabold uppercase tracking-wider text-hw-gray-500">Member</div>
        <div v-for="lang in languages" :key="lang" class="text-center text-[11px] font-extrabold uppercase tracking-wider text-hw-gray-500">
          {{ langLabels[lang] }}
        </div>
      </div>

      <!-- Matrix Rows -->
      <div class="space-y-1.5">
        <div
          v-for="m in memberStore.members"
          :key="m.id"
          class="grid grid-cols-4 gap-3 rounded-lg border p-2.5 transition-all hover:border-hw-red-200"
          style="border-color: #DDE1E8; background: #F7F8FA;"
        >
          <div class="flex items-center gap-2">
            <div class="h-7 w-7 rounded-full overflow-hidden border-2 flex-shrink-0" style="border-color: #CE0E2D; box-shadow: 0 0 0 1px #fff, 0 0 6px rgba(206,14,45,0.2);">
              <img :src="m.photo_url || `https://api.dicebear.com/7.x/bottts/svg?seed=${m.avatar_seed}`" class="h-full w-full object-cover" />
            </div>
            <span class="text-sm font-extrabold text-hw-gray-800 truncate">{{ m.name }}</span>
          </div>

          <div v-for="lang in languages" :key="lang" class="flex flex-col items-center justify-center gap-1">
            <span class="text-[11px] font-extrabold" :class="m.languages[lang] === 'N/A' ? 'text-hw-gray-400' : 'text-hw-gray-800'">
              {{ m.languages[lang] }}
            </span>
            <div class="w-full h-1.5 rounded-full overflow-hidden" style="background: #DDE1E8;">
              <div
                class="h-full rounded-full transition-all duration-500"
                :style="{ width: `${langLevels[m.languages[lang]] || 0}%`, background: langBarColors[m.languages[lang]] || '#C5CAD5' }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Language Distribution -->
    <div class="grid grid-cols-1 gap-4 lg:grid-cols-3">
      <div v-for="lang in languages" :key="lang" class="geo-card p-4 animate-slide-up" style="animation-delay: 100ms">
        <h3 class="mb-3 text-sm font-extrabold uppercase tracking-wider text-hw-red-600">{{ langLabels[lang] }}</h3>
        <div class="space-y-2">
          <div v-for="level in ['Native', 'Fluent', 'Professional', 'Intermediate', 'Basic']" :key="level" class="flex items-center justify-between">
            <span class="text-xs font-bold text-hw-gray-700">{{ level }}</span>
            <div class="flex items-center gap-2">
              <div class="h-1.5 w-20 rounded-full overflow-hidden" style="background: #DDE1E8;">
                <div
                  class="h-full rounded-full"
                  :style="{
                    width: `${memberStore.members.filter(m => m.languages[lang] === level).length / Math.max(memberStore.members.length, 1) * 100}%`,
                    background: langBarColors[level] || '#C5CAD5',
                  }"
                ></div>
              </div>
              <span class="text-xs font-extrabold font-mono text-hw-gray-600">
                {{ memberStore.members.filter(m => m.languages[lang] === level).length }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
