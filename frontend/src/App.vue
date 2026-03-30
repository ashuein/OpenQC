<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import {
  LayoutDashboard,
  Activity,
  TrendingUp,
  ClipboardCheck,
  Shield,
  Package,
  BookOpen,
  Settings,
} from 'lucide-vue-next'

const route = useRoute()

const navItems = [
  { to: '/', name: 'Dashboard', icon: LayoutDashboard },
  { to: '/qc', name: 'QC Monitor', icon: Activity },
  { to: '/sigma', name: 'Sigma Analysis', icon: TrendingUp },
  { to: '/validation', name: 'Validation', icon: ClipboardCheck },
  { to: '/audit', name: 'Audit Trail', icon: Shield },
  { to: '/lots', name: 'Lot Registry', icon: Package },
  { to: '/regulatory', name: 'Regulatory', icon: BookOpen },
]

const bottomNavItems = [
  { to: '/settings', name: 'Settings', icon: Settings },
]

function isActive(item) {
  if (item.to === '/') return route.path === '/'
  return route.path.startsWith(item.to)
}
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="sidebar-header">
        <span class="logo-text">OpenQC</span>
      </div>
      <nav class="sidebar-nav">
        <router-link
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="nav-link"
          :class="{ 'nav-link--active': isActive(item) }"
        >
          <component :is="item.icon" :size="18" :stroke-width="1.75" />
          <span>{{ item.name }}</span>
        </router-link>
      </nav>
      <div class="sidebar-bottom">
        <nav class="sidebar-nav">
          <router-link
            v-for="item in bottomNavItems"
            :key="item.to"
            :to="item.to"
            class="nav-link"
            :class="{ 'nav-link--active': isActive(item) }"
          >
            <component :is="item.icon" :size="18" :stroke-width="1.75" />
            <span>{{ item.name }}</span>
          </router-link>
        </nav>
      </div>
    </aside>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  display: flex;
  min-height: 100vh;
  min-height: 100dvh;
}

.sidebar {
  width: 240px;
  flex-shrink: 0;
  background-color: var(--bg-surface);
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--border-subtle);
}

.sidebar-header {
  padding: 20px 20px 16px;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 0 8px;
}

.sidebar-bottom {
  margin-top: auto;
  padding-top: 8px;
  padding-bottom: 12px;
  border-top: 1px solid var(--border-subtle);
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 12px;
  border-radius: 6px;
  color: var(--text-muted);
  text-decoration: none;
  font-size: 14px;
  font-weight: 450;
  transition: color 0.15s ease, background-color 0.15s ease;
}

.nav-link:hover {
  color: var(--text-secondary);
  background-color: var(--bg-surface-2);
}

.nav-link--active {
  color: var(--text-primary);
  background-color: var(--bg-highlight);
}

.content {
  flex: 1;
  min-width: 0;
  background-color: var(--bg-app);
  overflow-y: auto;
}
</style>
