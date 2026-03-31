<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import ChapterIntro from '@/components/learn/ChapterIntro.vue'
import ChapterWestgard from '@/components/learn/ChapterWestgard.vue'
import ChapterSigma from '@/components/learn/ChapterSigma.vue'
import ChapterValidation from '@/components/learn/ChapterValidation.vue'
import ChapterAudit from '@/components/learn/ChapterAudit.vue'
import ChapterUsingOpenQC from '@/components/learn/ChapterUsingOpenQC.vue'
import ChapterExamples from '@/components/learn/ChapterExamples.vue'

const route = useRoute()
const router = useRouter()

const chapters = [
  { id: 'intro', number: 1, title: 'Introduction to QC in PCR Labs', component: ChapterIntro },
  { id: 'westgard', number: 2, title: 'Westgard Rules Explained', component: ChapterWestgard },
  { id: 'sigma', number: 3, title: 'Six Sigma in the Laboratory', component: ChapterSigma },
  { id: 'validation', number: 4, title: 'Assay Validation Fundamentals', component: ChapterValidation },
  { id: 'audit', number: 5, title: 'Audit Trail & Compliance', component: ChapterAudit },
  { id: 'using-openqc', number: 6, title: 'Using OpenQC — Step by Step', component: ChapterUsingOpenQC },
  { id: 'examples', number: 7, title: 'Example Datasets Reference', component: ChapterExamples },
]

const activeChapter = ref(route.query.chapter || 'intro')

watch(() => route.query.chapter, (val) => {
  if (val) activeChapter.value = val
})

function selectChapter(id) {
  activeChapter.value = id
  router.replace({ query: { chapter: id } })
  const contentEl = document.querySelector('.learn-main')
  if (contentEl) contentEl.scrollTop = 0
}

function getActiveComponent() {
  const chapter = chapters.find(c => c.id === activeChapter.value)
  return chapter ? chapter.component : ChapterIntro
}

function navigateChapter(direction) {
  const currentIndex = chapters.findIndex(c => c.id === activeChapter.value)
  const nextIndex = currentIndex + direction
  if (nextIndex >= 0 && nextIndex < chapters.length) {
    selectChapter(chapters[nextIndex].id)
  }
}

function getCurrentIndex() {
  return chapters.findIndex(c => c.id === activeChapter.value)
}
</script>

<template>
  <div class="learn-layout">
    <aside class="learn-sidebar">
      <div class="learn-sidebar__title">Documentation</div>
      <nav class="learn-sidebar__nav">
        <button
          v-for="chapter in chapters"
          :key="chapter.id"
          class="learn-sidebar__item"
          :class="{ 'learn-sidebar__item--active': activeChapter === chapter.id }"
          @click="selectChapter(chapter.id)"
        >
          <span class="learn-sidebar__number">{{ chapter.number }}</span>
          <span class="learn-sidebar__label">{{ chapter.title }}</span>
        </button>
      </nav>
    </aside>
    <main class="learn-main">
      <component :is="getActiveComponent()" />
      <div class="learn-nav-footer">
        <button
          v-if="getCurrentIndex() > 0"
          class="learn-nav-btn learn-nav-btn--prev"
          @click="navigateChapter(-1)"
        >
          <span class="learn-nav-btn__direction">Previous</span>
          <span class="learn-nav-btn__title">{{ chapters[getCurrentIndex() - 1].title }}</span>
        </button>
        <div v-else />
        <button
          v-if="getCurrentIndex() < chapters.length - 1"
          class="learn-nav-btn learn-nav-btn--next"
          @click="navigateChapter(1)"
        >
          <span class="learn-nav-btn__direction">Next</span>
          <span class="learn-nav-btn__title">{{ chapters[getCurrentIndex() + 1].title }}</span>
        </button>
      </div>
    </main>
  </div>
</template>

<style scoped>
.learn-layout {
  display: flex;
  height: 100%;
  overflow: hidden;
}

/* Sidebar */
.learn-sidebar {
  width: 260px;
  flex-shrink: 0;
  background: var(--bg-surface);
  border-right: 1px solid var(--border-subtle);
  padding: 24px 0;
  overflow-y: auto;
}

.learn-sidebar__title {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  padding: 0 20px;
  margin-bottom: 16px;
}

.learn-sidebar__nav {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.learn-sidebar__item {
  display: flex;
  align-items: baseline;
  gap: 10px;
  padding: 8px 20px;
  cursor: pointer;
  font-size: 14px;
  color: var(--text-muted);
  transition: color 0.15s, background-color 0.15s;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  line-height: 1.4;
}

.learn-sidebar__item:hover {
  color: var(--text-secondary);
  background: var(--bg-surface-2);
}

.learn-sidebar__item--active {
  color: var(--text-primary);
  background: var(--bg-highlight);
}

.learn-sidebar__number {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  min-width: 18px;
  flex-shrink: 0;
}

.learn-sidebar__item--active .learn-sidebar__number {
  color: var(--text-secondary);
}

.learn-sidebar__label {
  flex: 1;
}

/* Main content area */
.learn-main {
  flex: 1;
  min-width: 0;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

/* Chapter navigation footer */
.learn-nav-footer {
  display: flex;
  justify-content: space-between;
  align-items: stretch;
  gap: 16px;
  padding: 24px 40px 48px;
  max-width: 860px;
  width: 100%;
  border-top: 1px solid var(--border-subtle);
  margin-top: auto;
}

.learn-nav-btn {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px 16px;
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  background: var(--bg-surface);
  cursor: pointer;
  transition: border-color 0.15s, background-color 0.15s;
  max-width: 280px;
}

.learn-nav-btn:hover {
  border-color: var(--border-strong);
  background: var(--bg-surface-2);
}

.learn-nav-btn--prev {
  text-align: left;
}

.learn-nav-btn--next {
  text-align: right;
  margin-left: auto;
}

.learn-nav-btn__direction {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.learn-nav-btn__title {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  line-height: 1.3;
}
</style>

<style>
/* Book-like content styling — unscoped so chapter components inherit */
.learn-content {
  max-width: 780px;
  padding: 32px 40px 80px;
  line-height: 1.75;
  color: var(--text-primary);
}

.learn-content .chapter-subtitle {
  font-size: 16px;
  color: var(--text-muted);
  margin-bottom: 32px;
  font-style: italic;
}

.learn-content h1 {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}

.learn-content h2 {
  font-size: 20px;
  font-weight: 600;
  margin-top: 40px;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-subtle);
  color: var(--text-primary);
}

.learn-content h3 {
  font-size: 16px;
  font-weight: 600;
  margin-top: 28px;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.learn-content p {
  margin-bottom: 16px;
  font-size: 15px;
  color: var(--text-secondary);
}

.learn-content ul,
.learn-content ol {
  margin-bottom: 16px;
  padding-left: 24px;
}

.learn-content li {
  margin-bottom: 6px;
  font-size: 15px;
  color: var(--text-secondary);
}

.learn-content strong {
  color: var(--text-primary);
  font-weight: 600;
}

.learn-content em {
  font-style: italic;
}

.learn-content code {
  background: var(--bg-surface-2);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
  font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace;
  color: var(--text-primary);
}

.learn-content pre {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 16px 20px;
  overflow-x: auto;
  margin-bottom: 20px;
}

.learn-content pre code {
  background: none;
  padding: 0;
  font-size: 13px;
  line-height: 1.6;
}

/* Info/tip boxes */
.learn-content .info-box {
  background: color-mix(in srgb, var(--color-success) 8%, var(--bg-surface));
  border-left: 3px solid var(--color-success);
  padding: 12px 16px;
  border-radius: 0 6px 6px 0;
  margin-bottom: 20px;
  font-size: 14px;
  color: var(--text-secondary);
}

.learn-content .info-box strong {
  color: var(--text-primary);
}

.learn-content .warning-box {
  background: color-mix(in srgb, var(--color-warning) 8%, var(--bg-surface));
  border-left: 3px solid var(--color-warning);
  padding: 12px 16px;
  border-radius: 0 6px 6px 0;
  margin-bottom: 20px;
  font-size: 14px;
  color: var(--text-secondary);
}

.learn-content .warning-box strong {
  color: var(--text-primary);
}

/* Diagrams rendered as styled pre blocks */
.learn-content .diagram {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 20px;
  font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace;
  font-size: 12px;
  line-height: 1.4;
  overflow-x: auto;
  margin-bottom: 20px;
  color: var(--text-secondary);
  white-space: pre;
}

/* Tables */
.learn-content table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  font-size: 14px;
}

.learn-content th {
  text-align: left;
  padding: 10px 12px;
  background: var(--bg-surface);
  border-bottom: 2px solid var(--border-strong);
  font-weight: 600;
  color: var(--text-primary);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.learn-content td {
  padding: 8px 12px;
  border-bottom: 1px solid var(--border-subtle);
  color: var(--text-secondary);
}

.learn-content td code {
  font-size: 12px;
}
</style>
