import { defineStore } from 'pinia'
import { ref } from 'vue'
import { projectsApi } from '@/api'
import type { Project, Assignment } from '@/types'

export const useProjectStore = defineStore('projects', () => {
  const projects = ref<Project[]>([])
  const calendarData = ref<Assignment[]>([])
  const loading = ref(false)

  async function fetchProjects() {
    loading.value = true
    try {
      const res = await projectsApi.list()
      projects.value = res.data
    } finally {
      loading.value = false
    }
  }

  async function fetchCalendar() {
    loading.value = true
    try {
      const res = await projectsApi.calendar()
      calendarData.value = res.data
    } finally {
      loading.value = false
    }
  }

  return { projects, calendarData, loading, fetchProjects, fetchCalendar }
})