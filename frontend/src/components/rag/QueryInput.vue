<script setup>
import { ref } from 'vue'
import { Button } from '@/components/ui/button'
import { Search } from 'lucide-vue-next'

defineProps({
  loading: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['submit'])

const question = ref('')

function handleSubmit() {
  const q = question.value.trim()
  if (!q) return
  emit('submit', q)
}
</script>

<template>
  <form class="query-input" @submit.prevent="handleSubmit">
    <div class="query-input__field-wrapper">
      <Search :size="16" :stroke-width="1.75" class="query-input__icon" />
      <input
        v-model="question"
        type="text"
        class="query-input__field"
        placeholder="Ask a regulatory question..."
        :disabled="disabled || loading"
      />
    </div>
    <Button
      size="sm"
      type="submit"
      :disabled="disabled || loading || !question.trim()"
    >
      {{ loading ? 'Searching...' : 'Ask' }}
    </Button>
  </form>
</template>

<style scoped>
.query-input {
  display: flex;
  gap: 10px;
  align-items: center;
}

.query-input__field-wrapper {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
}

.query-input__icon {
  position: absolute;
  left: 12px;
  color: var(--text-muted);
  pointer-events: none;
}

.query-input__field {
  width: 100%;
  height: 38px;
  padding: 0 12px 0 36px;
  border-radius: 6px;
  border: 1px solid var(--border-subtle);
  background-color: var(--bg-surface-2);
  color: var(--text-primary);
  font-size: 14px;
  font-family: inherit;
  outline: none;
  transition: border-color 0.15s ease;
}

.query-input__field::placeholder {
  color: var(--text-muted);
  opacity: 0.6;
}

.query-input__field:focus {
  border-color: var(--border-strong);
}

.query-input__field:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
