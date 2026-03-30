<script setup>
import { onMounted } from 'vue'
import { useRAGStore } from '@/stores/ragStore'
import PageHeader from '@/components/shared/PageHeader.vue'
import IngestionStatus from '@/components/rag/IngestionStatus.vue'
import QueryInput from '@/components/rag/QueryInput.vue'
import AnswerCard from '@/components/rag/AnswerCard.vue'
import { Button } from '@/components/ui/button'
import { MessageSquare } from 'lucide-vue-next'

const store = useRAGStore()

const isCorpusReady = () =>
  store.status && store.status.status === 'ready'

async function handleIngest() {
  try {
    await store.ingest()
  } catch {
    // error shown via store
  }
}

async function handleQuery(question) {
  try {
    await store.ask(question)
  } catch {
    // error shown via store
  }
}

onMounted(() => {
  store.loadStatus()
})
</script>

<template>
  <div class="view">
    <PageHeader
      title="Regulatory Assistant"
      subtitle="AI-powered regulatory guidance and document search"
    />

    <div class="rag-content">
      <!-- Ingestion status -->
      <IngestionStatus
        :status="store.status"
        :ingesting="store.ingesting"
        @ingest="handleIngest"
      />

      <!-- Query input -->
      <div class="query-section">
        <QueryInput
          :loading="store.loading"
          :disabled="!isCorpusReady() && !store.ingesting"
          @submit="handleQuery"
        />
      </div>

      <!-- Error display -->
      <div v-if="store.error" class="error-strip">
        <p class="error-strip__text">{{ store.error }}</p>
        <Button variant="ghost" size="sm" @click="store.clearError()">Dismiss</Button>
      </div>

      <!-- Answer card -->
      <div v-if="store.answer" class="answer-section">
        <AnswerCard
          :answer="store.answer.answer"
          :sources="store.answer.sources || []"
          :model-used="store.answer.model_used || ''"
        />
      </div>

      <!-- Empty state (no query yet) -->
      <div
        v-if="!store.answer && !store.loading && !store.error"
        class="empty-state"
      >
        <MessageSquare :size="28" :stroke-width="1.25" class="empty-state__icon" />
        <p class="empty-state__text">
          Ask a question about regulatory standards, compliance requirements, or QC guidelines.
        </p>
      </div>

      <!-- Loading indicator -->
      <div v-if="store.loading" class="loading-state">
        <div class="loading-state__bar"></div>
        <p class="loading-state__text">Searching regulatory documents...</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.view {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.rag-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 24px 28px;
  max-width: 800px;
}

.query-section {
  /* no extra styling needed */
}

.error-strip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  border-radius: 6px;
  background-color: color-mix(in srgb, var(--color-danger) 8%, transparent);
  border: 1px solid color-mix(in srgb, var(--color-danger) 20%, transparent);
}

.error-strip__text {
  font-size: 13px;
  color: var(--color-danger);
}

.answer-section {
  /* no extra styling needed */
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 48px 16px;
}

.empty-state__icon {
  color: var(--text-muted);
  opacity: 0.5;
}

.empty-state__text {
  font-size: 14px;
  color: var(--text-muted);
  text-align: center;
  max-width: 440px;
  line-height: 1.5;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 32px 16px;
}

.loading-state__bar {
  width: 120px;
  height: 2px;
  border-radius: 1px;
  background-color: var(--bg-highlight);
  position: relative;
  overflow: hidden;
}

.loading-state__bar::after {
  content: '';
  position: absolute;
  top: 0;
  left: -40%;
  width: 40%;
  height: 100%;
  background-color: var(--text-muted);
  animation: loading-slide 1.2s ease-in-out infinite;
}

@keyframes loading-slide {
  0% { left: -40%; }
  100% { left: 100%; }
}

.loading-state__text {
  font-size: 13px;
  color: var(--text-muted);
}
</style>
