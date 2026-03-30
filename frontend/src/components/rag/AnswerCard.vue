<script setup>
import { ref } from 'vue'
import { FileText, ChevronDown, ChevronUp } from 'lucide-vue-next'

defineProps({
  answer: {
    type: String,
    required: true,
  },
  sources: {
    type: Array,
    default: () => [],
  },
  modelUsed: {
    type: String,
    default: '',
  },
})

const expandedSource = ref(null)

function toggleSource(index) {
  expandedSource.value = expandedSource.value === index ? null : index
}
</script>

<template>
  <div class="answer-card">
    <div class="answer-card__body">
      <p class="answer-card__text">{{ answer }}</p>
    </div>

    <div v-if="sources.length > 0" class="answer-card__sources">
      <div class="answer-card__sources-label">Sources</div>
      <div class="answer-card__source-list">
        <div
          v-for="(source, idx) in sources"
          :key="idx"
          class="source-chip-wrapper"
        >
          <button
            class="source-chip"
            :class="{ 'source-chip--expanded': expandedSource === idx }"
            @click="toggleSource(idx)"
          >
            <FileText :size="13" :stroke-width="1.75" />
            <span class="source-chip__name">{{ source.document_name }}</span>
            <span v-if="source.page_number" class="source-chip__page">
              p.{{ source.page_number }}
            </span>
            <component
              :is="expandedSource === idx ? ChevronUp : ChevronDown"
              :size="12"
              :stroke-width="1.75"
              class="source-chip__chevron"
            />
          </button>
          <div v-if="expandedSource === idx" class="source-preview">
            <p v-if="source.section" class="source-preview__section">
              {{ source.section }}
            </p>
            <p class="source-preview__text">
              {{ source.chunk_preview || 'No preview available.' }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <div v-if="modelUsed" class="answer-card__meta">
      Model: {{ modelUsed }}
    </div>
  </div>
</template>

<style scoped>
.answer-card {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 6px;
  overflow: hidden;
}

.answer-card__body {
  padding: 20px;
}

.answer-card__text {
  font-size: 14px;
  line-height: 1.7;
  color: var(--text-primary);
  white-space: pre-wrap;
}

.answer-card__sources {
  padding: 16px 20px;
  border-top: 1px solid var(--border-subtle);
}

.answer-card__sources-label {
  font-size: 11px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 10px;
}

.answer-card__source-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.source-chip-wrapper {
  display: flex;
  flex-direction: column;
}

.source-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 10px;
  border-radius: 4px;
  border: 1px solid var(--border-subtle);
  background-color: var(--bg-surface-2);
  color: var(--text-secondary);
  font-size: 12px;
  font-family: inherit;
  cursor: pointer;
  transition: background-color 0.15s ease, border-color 0.15s ease;
  white-space: nowrap;
  width: fit-content;
}

.source-chip:hover {
  border-color: var(--border-strong);
  background-color: var(--bg-highlight);
}

.source-chip--expanded {
  border-color: var(--border-strong);
}

.source-chip__name {
  font-weight: 500;
  color: var(--text-primary);
}

.source-chip__page {
  color: var(--text-muted);
  font-variant-numeric: tabular-nums;
}

.source-chip__chevron {
  color: var(--text-muted);
  margin-left: 2px;
}

.source-preview {
  margin-top: 4px;
  margin-left: 10px;
  padding: 10px 12px;
  background-color: var(--bg-surface-2);
  border-radius: 4px;
  border: 1px solid var(--border-subtle);
}

.source-preview__section {
  font-size: 11px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.03em;
  margin-bottom: 6px;
}

.source-preview__text {
  font-size: 13px;
  line-height: 1.6;
  color: var(--text-secondary);
}

.answer-card__meta {
  padding: 10px 20px;
  border-top: 1px solid var(--border-subtle);
  font-size: 11px;
  color: var(--text-muted);
}
</style>
