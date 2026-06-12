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
      name: 'Calendar',
      component: () => import('@/views/CalendarView.vue'),
    },
    {
      path: '/admin',
      name: 'Admin',
      component: () => import('@/views/AdminView.vue'),
    },
  ],
})

export default router
