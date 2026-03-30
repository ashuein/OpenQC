<script setup>
import { computed } from 'vue'
import { CheckCircle2, AlertCircle, Loader2, Upload, FileSpreadsheet } from 'lucide-vue-next'

const props = defineProps({
  status: {
    type: String,
    default: 'idle',
    validator: (v) => ['idle', 'uploading', 'parsing', 'complete', 'error'].includes(v),
  },
  fileName: {
    type: String,
    default: '',
  },
  message: {
    type: String,
    default: '',
  },
})

const statusConfig = computed(() => {
  const configs = {
    idle: {
      icon: FileSpreadsheet,
      label: 'Ready',
      colorClass: 'progress--idle',
      spinning: false,
    },
    uploading: {
      icon: Upload,
      label: 'Uploading...',
      colorClass: 'progress--uploading',
      spinning: true,
    },
    parsing: {
      icon: Loader2,
      label: 'Parsing...',
      colorClass: 'progress--parsing',
      spinning: true,
    },
    complete: {
      icon: CheckCircle2,
      label: 'Complete',
      colorClass: 'progress--complete',
      spinning: false,
    },
    error: {
      icon: AlertCircle,
      label: 'Error',
      colorClass: 'progress--error',
      spinning: false,
    },
  }
  return configs[props.status] || configs.idle
})
</script>

<template>
  <div class="progress" :class="statusConfig.colorClass">
    <div class="progress__row">
      <component
        :is="statusConfig.icon"
        :size="18"
        :stroke-width="1.75"
        class="progress__icon"
        :class="{ 'progress__icon--spin': statusConfig.spinning }"
      />
      <span class="progress__label">{{ statusConfig.label }}</span>
    </div>
    <span v-if="fileName" class="progress__filename">{{ fileName }}</span>
    <span v-if="message" class="progress__message">{{ message }}</span>
  </div>
</template>

<style scoped>
.progress {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px 16px;
  border-radius: 6px;
  background-color: var(--bg-surface);
  border: 1px solid var(--border-subtle);
}

.progress__row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.progress__icon {
  flex-shrink: 0;
}

.progress__icon--spin {
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.progress__label {
  font-size: 13px;
  font-weight: 500;
}

.progress__filename {
  font-size: 12px;
  color: var(--text-muted);
  padding-left: 26px;
}

.progress__message {
  font-size: 12px;
  padding-left: 26px;
}

/* Status colors */
.progress--idle .progress__icon,
.progress--idle .progress__label {
  color: var(--text-muted);
}

.progress--uploading .progress__icon,
.progress--uploading .progress__label,
.progress--parsing .progress__icon,
.progress--parsing .progress__label {
  color: var(--text-secondary);
}

.progress--complete .progress__icon,
.progress--complete .progress__label {
  color: var(--color-success);
}

.progress--error .progress__icon,
.progress--error .progress__label {
  color: var(--color-danger);
}

.progress--error .progress__message {
  color: var(--color-danger);
}

.progress--complete .progress__message {
  color: var(--color-success);
}
</style>
