import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// ── Auth interceptor ──
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
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

// ── Auth ──
export const authApi = {
  login: (username: string, password: string) => api.post('/auth/login', { username, password }),
  me: () => api.get('/auth/me'),
}

// ── Skills ──
export const skillsApi = {
  list: () => api.get('/skills/'),
  create: (data: { name: string; category: string }) => api.post('/skills/', data),
  update: (id: number, data: { name?: string; category?: string }) => api.put(`/skills/${id}`, data),
  delete: (id: number) => api.delete(`/skills/${id}`),
}

// ── Certificate Templates ──
export const certTemplatesApi = {
  list: () => api.get('/cert-templates/'),
  create: (data: { name: string; category: string }) => api.post('/cert-templates/', data),
  update: (id: number, data: { name?: string; category?: string }) => api.put(`/cert-templates/${id}`, data),
  delete: (id: number) => api.delete(`/cert-templates/${id}`),
}

// ── Admin Users ──
export const adminsApi = {
  list: () => api.get('/admins/'),
  create: (data: { username: string; password: string }) => api.post('/admins/', data),
  delete: (id: number) => api.delete(`/admins/${id}`),
}

export default api
