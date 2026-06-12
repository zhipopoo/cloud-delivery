<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useMemberStore } from '@/stores/members'
import { useProjectStore } from '@/stores/projects'
import MemberProfileCard from '@/components/MemberProfileCard.vue'

const memberStore = useMemberStore()
const projectStore = useProjectStore()
const selectedMemberId = ref<number | null>(null)

onMounted(async () => {
  await memberStore.fetchMembers()
  await projectStore.fetchCalendar()
})

const selectedMember = computed(() =>
  memberStore.members.find(m => m.id === selectedMemberId.value) || null
)

const groupedMembers = computed(() => {
  const groups: Record<string, typeof memberStore.members> = {}
  for (const m of memberStore.members) {
    if (!groups[m.team]) groups[m.team] = []
    groups[m.team].push(m)
  }
  return groups
})

const teamLabels: Record<string, string> = {
  TMO: 'Technical TMO',
  PMO: 'Project Management PMO',
  Management: 'Management Team',
}
</script>

<template>
  <div class="space-y-6">
    <div v-for="(members, team) in groupedMembers" :key="team" class="animate-slide-up">
      <div class="mb-3 flex items-center gap-3">
        <div class="h-px flex-1 bg-gradient-to-r from-hw-red-200 to-transparent"></div>
        <h2 class="text-sm font-extrabold uppercase tracking-widest text-hw-red-600">{{ teamLabels[team] || team }}</h2>
        <div class="h-px flex-1 bg-gradient-to-l from-hw-red-200 to-transparent"></div>
      </div>

      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="m in members"
          :key="m.id"
          class="geo-card-hover cursor-pointer p-4"
          @click="selectedMemberId = m.id"
        >
          <div class="flex items-start gap-4">
            <div class="avatar-hex h-14 w-14 flex-shrink-0 overflow-hidden">
              <img
                :src="m.photo_url || `https://api.dicebear.com/7.x/bottts/svg?seed=${m.avatar_seed}`"
                :alt="m.name"
                class="h-full w-full object-cover"
              />
            </div>
            <div class="min-w-0 flex-1">
              <h3 class="text-base font-extrabold text-hw-gray-800">{{ m.name }}</h3>
              <p class="text-xs font-semibold text-hw-gray-500">{{ m.title }}</p>
              <div class="mt-2 flex flex-wrap gap-1">
                <span class="geo-badge text-[10px]">{{ m.team }}</span>
                <span class="geo-badge text-[10px]">{{ m.role }}</span>
              </div>
            </div>
          </div>
          <p class="mt-3 line-clamp-2 text-xs text-hw-gray-600">{{ m.bio }}</p>
          <!-- Skills -->
          <div class="mt-3 flex flex-wrap items-center gap-1">
            <span
              v-for="skill in m.skills.slice(0, 4)"
              :key="skill"
              class="rounded px-1.5 py-0.5 text-[10px] font-semibold"
              style="background: #FFF0F2; color: #CE0E2D; border: 1px solid #FFD6DB;"
            >{{ skill }}</span>
            <span v-if="m.skills.length > 4" class="text-[10px] font-bold text-hw-gray-400">
              +{{ m.skills.length - 4 }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <MemberProfileCard
      v-if="selectedMember"
      :member="selectedMember"
      @close="selectedMemberId = null"
    />
  </div>
</template>
