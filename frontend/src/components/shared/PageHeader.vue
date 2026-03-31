<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <header class="page-header">
    <div class="page-header__text">
      <h1 class="page-header__title">{{ title }}</h1>
      <p v-if="subtitle" class="page-header__subtitle">{{ subtitle }}</p>
    </div>
    <div class="page-header__actions">
      <slot name="actions" />
    </div>
  </header>
</template>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 24px 32px 20px 28px;
  border-bottom: 1px solid var(--border-subtle);
}

.page-header__text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.page-header__title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.page-header__subtitle {
  font-size: 14px;
  color: var(--text-muted);
  font-weight: 400;
}

.page-header__actions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 8px;
  flex-shrink: 0;
  max-width: 50%;
  padding-right: 4px;
}
</style>
