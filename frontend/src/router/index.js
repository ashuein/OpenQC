import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: () => import('../views/DashboardView.vue'),
  },
  {
    path: '/qc',
    name: 'qc-monitor',
    component: () => import('../views/QCMonitorView.vue'),
  },
  {
    path: '/sigma',
    name: 'sigma',
    component: () => import('../views/SigmaView.vue'),
  },
  {
    path: '/validation',
    name: 'validation',
    component: () => import('../views/ValidatorView.vue'),
  },
  {
    path: '/audit',
    name: 'audit',
    component: () => import('../views/AuditView.vue'),
  },
  {
    path: '/lots',
    name: 'lot-registry',
    component: () => import('../views/LotRegistryView.vue'),
  },
  {
    path: '/regulatory',
    name: 'regulatory-assistant',
    component: () => import('../views/RegulatoryAssistantView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
