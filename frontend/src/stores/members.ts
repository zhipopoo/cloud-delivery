import { defineStore } from 'pinia'
import { ref } from 'vue'
import { membersApi } from '@/api'
import type { Member } from '@/types'

export const useMemberStore = defineStore('members', () => {
  const members = ref<Member[]>([])
  const loading = ref(false)
  const selectedTeam = ref<string | null>(null)
  const selectedMember = ref<Member | null>(null)

  async function fetchMembers(team?: string) {
    loading.value = true
    try {
      const res = await membersApi.list(team)
      members.value = res.data
    } finally {
      loading.value = false
    }
  }

  async function fetchMember(id: number) {
    const res = await membersApi.get(id)
    selectedMember.value = res.data
  }

  function filterByTeam(team: string | null) {
    selectedTeam.value = team
    fetchMembers(team || undefined)
  }

  return { members, loading, selectedTeam, selectedMember, fetchMembers, fetchMember, filterByTeam }
})