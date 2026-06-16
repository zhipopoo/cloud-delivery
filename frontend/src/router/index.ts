import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/dashboard',
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('@/views/DashboardView.vue'),
    },
    {
      path: '/team',
      name: 'Team',
      component: () => import('@/views/TeamView.vue'),
    },
    {
      path: '/skills',
      name: 'Skills',
      component: () => import('@/views/SkillsView.vue'),
    },
    {
      path: '/certificates',
      name: 'Certificates',
      component: () => import('@/views/CertificatesView.vue'),
    },
    {
      path: '/languages',
      name: 'Languages',
      component: () => import('@/views/LanguagesView.vue'),
    },
    {
      path: '/fans',
      name: 'Fans',
      component: () => import('@/views/FansView.vue'),
    },
    {
      path: '/calendar',
      redirect: '/calendar/personnel',
    },
    {
      path: '/calendar/personnel',
      name: 'CalendarPersonnel',
      component: () => import('@/views/CalendarByPersonView.vue'),
    },
    {
      path: '/calendar/projects',
      name: 'CalendarProjects',
      component: () => import('@/views/CalendarByProjectView.vue'),
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/admin',
      redirect: '/admin/members',
    },
    {
      path: '/admin/members',
      name: 'AdminMembers',
      component: () => import('@/views/admin/AdminMembersView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/admin/projects',
      name: 'AdminProjects',
      component: () => import('@/views/admin/AdminProjectsView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/admin/skills',
      name: 'AdminSkills',
      component: () => import('@/views/admin/AdminSkillsView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/admin/certificates',
      name: 'AdminCertificates',
      component: () => import('@/views/admin/AdminCertificatesView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/admin/admins',
      name: 'AdminAdmins',
      component: () => import('@/views/admin/AdminAdminsView.vue'),
      meta: { requiresAuth: true },
    },
  ],
})

// Global auth guard
router.beforeEach((to, _from, next) => {
  if (to.matched.some(r => r.meta.requiresAuth)) {
    const token = localStorage.getItem('admin_token')
    if (!token) {
      next({ name: 'Login', query: { redirect: to.fullPath } })
      return
    }
  }
  next()
})

export default router
