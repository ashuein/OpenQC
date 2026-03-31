<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'default',
    validator: (v) => ['default', 'destructive', 'outline', 'ghost', 'link'].includes(v),
  },
  size: {
    type: String,
    default: 'default',
    validator: (v) => ['default', 'sm', 'lg', 'icon'].includes(v),
  },
  disabled: {
    type: Boolean,
    default: false,
  },
})

const btnClass = computed(() => {
  const classes = ['btn', `btn--${props.variant}`, `btn--${props.size}`]
  if (props.disabled) classes.push('btn--disabled')
  return classes.join(' ')
})
</script>

<template>
  <button :class="btnClass" :disabled="disabled">
    <slot />
  </button>
</template>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  white-space: nowrap;
  border-radius: 6px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  transition: color 0.15s ease, background-color 0.15s ease, border-color 0.15s ease;
  border: 1px solid transparent;
  line-height: 1;
}

.btn:focus-visible {
  outline: 2px solid var(--border-strong);
  outline-offset: 2px;
}

/* Sizes */
.btn--default {
  height: 36px;
  padding: 0 16px;
  font-size: 14px;
}

.btn--sm {
  height: 32px;
  padding: 0 14px;
  font-size: 13px;
}

.btn--lg {
  height: 40px;
  padding: 0 24px;
  font-size: 15px;
}

.btn--icon {
  height: 36px;
  width: 36px;
  padding: 0;
  font-size: 14px;
}

/* Variants */
.btn--default {
  background-color: var(--bg-highlight);
  color: var(--text-primary);
  border-color: var(--border-strong);
}

.btn--default:hover:not(:disabled) {
  background-color: var(--border-subtle);
}

.btn--destructive {
  background-color: var(--color-danger);
  color: #ffffff;
  border-color: var(--color-danger);
}

.btn--destructive:hover:not(:disabled) {
  opacity: 0.9;
}

.btn--outline {
  background-color: transparent;
  color: var(--text-secondary);
  border-color: var(--border-strong);
}

.btn--outline:hover:not(:disabled) {
  background-color: var(--bg-surface-2);
  color: var(--text-primary);
  border-color: var(--text-muted);
}

.btn--ghost {
  background-color: transparent;
  color: var(--text-secondary);
  border-color: transparent;
}

.btn--ghost:hover:not(:disabled) {
  background-color: var(--bg-surface-2);
  color: var(--text-primary);
}

.btn--link {
  background-color: transparent;
  color: var(--text-secondary);
  border-color: transparent;
  text-decoration: underline;
  text-underline-offset: 4px;
}

.btn--link:hover:not(:disabled) {
  color: var(--text-primary);
}

/* Disabled */
.btn--disabled,
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}
</style>
