<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useMemberStore } from '@/stores/members'
import type { Member } from '@/types'

const memberStore = useMemberStore()
const selectedMember = ref<Member | null>(null)

onMounted(async () => {
  await memberStore.fetchMembers()
})

const skillCategories: Record<string, string[]> = {
  'Cloud & Infra': ['Kubernetes', 'Docker', 'Terraform', 'Ansible', 'CCE', 'Huawei Cloud', 'CI/CD', 'Jenkins'],
  'Project & Process': ['Project Governance', 'Risk Management', 'Agile', 'SAFe', 'Jira', 'Confluence', 'MS Project', 'Stakeholder Management'],
  'Security & Compliance': ['Cloud Security', 'Compliance', 'WAF', 'DDoS Protection', 'Network Security', 'ISO 27001'],
  'Data & AI': ['Python', 'Big Data', 'AI Model'],
  'Business': ['Strategic Planning', 'Client Relations', 'Digital Transformation', 'Budget Control', 'Cloud Migration'],
}

function getMembersWithSkill(skill: string): Member[] {
  return memberStore.members.filter(m => m.skills.includes(skill))
}

const accentBars = ['bg-hw-red-600', 'bg-hw-red-400', 'bg-hw-red-500', 'bg-hw-gold-500']
</script>

<template>
  <div class="space-y-5">
    <div v-for="(skills, category, idx) in skillCategories" :key="category" class="geo-card p-4 animate-slide-up" :style="{ animationDelay: `${idx * 60}ms` }">
      <div class="mb-3 flex items-center gap-3">
        <div class="h-1 w-6 rounded-full" :class="accentBars[idx % accentBars.length]"></div>
        <h2 class="text-sm font-extrabold uppercase tracking-wider text-hw-gray-800">{{ category }}</h2>
        <span class="geo-badge text-[10px]">{{ skills.length }} skills</span>
      </div>

      <div class="grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        <div
          v-for="skill in skills"
          :key="skill"
          class="group rounded-lg border p-3 transition-all hover:border-hw-red-300 hover:shadow-sm cursor-default"
          style="border-color: #DDE1E8; background: #F7F8FA;"
        >
          <div class="flex items-center justify-between">
            <span class="text-sm font-extrabold text-hw-gray-800">{{ skill }}</span>
            <span class="text-[11px] font-bold text-hw-red-600">{{ getMembersWithSkill(skill).length }}人</span>
          </div>
          <div class="mt-2 flex flex-wrap gap-1">
            <div
              v-for="m in getMembersWithSkill(skill)"
              :key="m.id"
              class="flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-bold cursor-pointer transition-colors hover:bg-hw-red-100"
              style="background: #FFF0F2; color: #CE0E2D;"
              @click="selectedMember = m"
            >
              <div class="h-3.5 w-3.5 rounded-full overflow-hidden border border-hw-red-200">
                <img :src="m.photo_url || `https://api.dicebear.com/7.x/bottts/svg?seed=${m.avatar_seed}`" class="h-full w-full" />
              </div>
              {{ m.name.split(' ')[0] }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Selected Member Modal -->
    <div v-if="selectedMember" class="fixed inset-0 z-50 flex items-center justify-center" style="background: rgba(15,19,30,0.6); backdrop-filter: blur(4px);">
      <div class="geo-card w-full max-w-lg p-5 animate-slide-up mx-4">
        <div class="flex items-start justify-between mb-4">
          <div class="flex items-center gap-3">
            <div class="avatar-hex h-14 w-14 flex-shrink-0 overflow-hidden">
              <img :src="selectedMember.photo_url || `https://api.dicebear.com/7.x/bottts/svg?seed=${selectedMember.avatar_seed}`" class="h-full w-full object-cover" />
            </div>
            <div>
              <h2 class="text-base font-extrabold text-hw-gray-800">{{ selectedMember.name }}</h2>
              <p class="text-xs font-semibold text-hw-gray-500">{{ selectedMember.title }}</p>
              <div class="mt-1 flex gap-1">
                <span class="geo-badge text-[10px]">{{ selectedMember.team }}</span>
                <span class="geo-badge text-[10px]">{{ selectedMember.role }}</span>
              </div>
            </div>
          </div>
          <button class="rounded p-1.5 hover:bg-gray-100 text-hw-gray-400 hover:text-hw-red-600 text-lg" @click="selectedMember = null">✕</button>
        </div>
        <p class="text-sm text-hw-gray-600 mb-4 leading-relaxed">{{ selectedMember.bio }}</p>
        <div>
          <h3 class="text-[11px] font-extrabold uppercase tracking-wider text-hw-gray-500 mb-2">Skills</h3>
          <div class="flex flex-wrap gap-1.5">
            <span v-for="s in selectedMember.skills" :key="s" class="geo-badge">{{ s }}</span>
          </div>
        </div>
        <div class="mt-4 pt-3 border-t flex items-center gap-4 text-xs" style="border-color: #DDE1E8;">
          <span class="text-hw-gray-500">WeLink：<strong class="text-hw-gray-800">{{ selectedMember.welink_id || '—' }}</strong></span>
          <span class="text-hw-gray-500">Certs：<strong class="text-hw-gray-800">{{ selectedMember.certificates.filter(c => c.status === 'active').length }}</strong></span>
          <span class="text-hw-gray-500">Fans：<strong class="text-hw-red-600">{{ selectedMember.fans_count }}</strong></span>
        </div>
      </div>
    </div>
  </div>
</template>
