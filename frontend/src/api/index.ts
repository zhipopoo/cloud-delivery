import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// ── Members ──
export const membersApi = {
  list: (team?: string) => api.get('/members/', { params: { team } }),
  get: (id: number) => api.get(`/members/${id}`),
  create: (data: any) => api.post('/members/', data),
  update: (id: number, data: any) => api.put(`/members/${id}`, data),
  delete: (id: number) => api.delete(`/members/${id}`),
}

// ── Projects ──
export const projectsApi = {
  list: () => api.get('/projects/'),
  create: (data: any) => api.post('/projects/', data),
  update: (id: number, data: any) => api.put(`/projects/${id}`, data),
  delete: (id: number) => api.delete(`/projects/${id}`),
  calendar: () => api.get('/projects/calendar'),
  assign: (data: any) => api.post('/projects/assign', data),
  updateAssignment: (id: number, data: any) => api.put(`/projects/assign/${id}`, data),
  deleteAssignment: (id: number) => api.delete(`/projects/assign/${id}`),
}

// ── Fans ──
export const fansApi = {
  getMessages: (memberId: number) => api.get(`/fans/${memberId}`),
  postMessage: (data: any) => api.post('/fans/', data),
}

// ── Uploads ──
export const uploadsApi = {
  upload: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/uploads/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}

export default api
