<script setup>
import { ref, watch, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { PanelRightClose, PanelRightOpen } from 'lucide-vue-next'

import ChapterIntro from '@/components/learn/ChapterIntro.vue'
import ChapterWestgard from '@/components/learn/ChapterWestgard.vue'
import ChapterSigma from '@/components/learn/ChapterSigma.vue'
import ChapterValidation from '@/components/learn/ChapterValidation.vue'
import ChapterAudit from '@/components/learn/ChapterAudit.vue'
import ChapterUsingOpenQC from '@/components/learn/ChapterUsingOpenQC.vue'
import ChapterExamples from '@/components/learn/ChapterExamples.vue'
import ChapterExperimentDesign from '@/components/learn/ChapterExperimentDesign.vue'

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
  { id: 'experiment-design', number: 8, title: 'Designing Experiments & Reports', component: ChapterExperimentDesign },
]

const activeChapter = ref(route.query.chapter || 'intro')
const tocCollapsed = ref(false)

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

function toggleToc() {
  tocCollapsed.value = !tocCollapsed.value
}
</script>

<template>
  <div class="learn-layout">
    <main class="learn-main" ref="mainRef">
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
    <aside class="learn-toc" :class="{ 'learn-toc--collapsed': tocCollapsed }">
      <div class="learn-toc__header">
        <span v-if="!tocCollapsed" class="learn-toc__title">Chapters</span>
        <button class="learn-toc__toggle" @click="toggleToc" :title="tocCollapsed ? 'Show chapters' : 'Hide chapters'">
          <PanelRightOpen v-if="tocCollapsed" :size="16" :stroke-width="1.75" />
          <PanelRightClose v-else :size="16" :stroke-width="1.75" />
        </button>
      </div>
      <nav v-if="!tocCollapsed" class="learn-toc__nav">
        <button
          v-for="chapter in chapters"
          :key="chapter.id"
          class="learn-toc__item"
          :class="{ 'learn-toc__item--active': activeChapter === chapter.id }"
          @click="selectChapter(chapter.id)"
        >
          <span class="learn-toc__number">{{ chapter.number }}</span>
          <span class="learn-toc__label">{{ chapter.title }}</span>
        </button>
      </nav>
      <nav v-else class="learn-toc__nav">
        <button
          v-for="chapter in chapters"
          :key="chapter.id"
          class="learn-toc__item learn-toc__item--icon"
          :class="{ 'learn-toc__item--active': activeChapter === chapter.id }"
          :title="chapter.title"
          @click="selectChapter(chapter.id)"
        >
          <span class="learn-toc__number">{{ chapter.number }}</span>
        </button>
      </nav>
    </aside>
  </div>
</template>

<style scoped>
.learn-layout {
  display: flex;
  height: 100vh;
  height: 100dvh;
  overflow: hidden;
}

/* Main content — scrollable, takes remaining space */
.learn-main {
  flex: 1;
  min-width: 0;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

/* Right-side table of contents */
.learn-toc {
  width: 260px;
  flex-shrink: 0;
  background: var(--bg-surface);
  border-left: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  transition: width 0.2s ease;
}

.learn-toc--collapsed {
  width: 48px;
}

.learn-toc__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 16px 12px;
  gap: 8px;
}

.learn-toc--collapsed .learn-toc__header {
  justify-content: center;
  padding: 16px 8px 12px;
}

.learn-toc__title {
  font-size: 16px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  white-space: nowrap;
}

.learn-toc__toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  background: none;
  color: var(--text-muted);
  cursor: pointer;
  border-radius: 6px;
  flex-shrink: 0;
  transition: color 0.15s, background-color 0.15s;
}

.learn-toc__toggle:hover {
  color: var(--text-secondary);
  background-color: var(--bg-surface-2);
}

.learn-toc__nav {
  display: flex;
  flex-direction: column;
  gap: 1px;
  padding: 0 8px;
}

.learn-toc--collapsed .learn-toc__nav {
  padding: 0 6px;
}

.learn-toc__item {
  display: flex;
  align-items: baseline;
  gap: 10px;
  padding: 10px 12px;
  cursor: pointer;
  font-size: 17px;
  color: var(--text-muted);
  transition: color 0.15s, background-color 0.15s;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  line-height: 1.4;
  border-radius: 6px;
}

.learn-toc__item--icon {
  justify-content: center;
  padding: 8px;
  gap: 0;
}

.learn-toc__item:hover {
  color: var(--text-secondary);
  background: var(--bg-surface-2);
}

.learn-toc__item--active {
  color: var(--text-primary);
  background: var(--bg-highlight);
}

.learn-toc__number {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-muted);
  min-width: 16px;
  flex-shrink: 0;
}

.learn-toc__item--active .learn-toc__number {
  color: var(--text-secondary);
}

.learn-toc__label {
  flex: 1;
}

/* Chapter navigation footer */
.learn-nav-footer {
  display: flex;
  justify-content: space-between;
  align-items: stretch;
  gap: 16px;
  padding: 24px 48px 48px;
  max-width: 960px;
  margin: auto auto 0;
  width: 100%;
  border-top: 1px solid var(--border-subtle);
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
  max-width: 320px;
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
  max-width: 960px;
  margin: 0 auto;
  padding: 32px 48px 80px;
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
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 8px;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}

.learn-content h2 {
  font-size: 24px;
  font-weight: 600;
  margin-top: 40px;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-subtle);
  color: var(--text-primary);
}

.learn-content h3 {
  font-size: 18px;
  font-weight: 600;
  margin-top: 28px;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.learn-content p {
  margin-bottom: 16px;
  font-size: 16px;
  color: var(--text-secondary);
}

.learn-content ul,
.learn-content ol {
  margin-bottom: 16px;
  padding-left: 24px;
}

.learn-content li {
  margin-bottom: 6px;
  font-size: 16px;
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
  font-size: 14px;
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
  font-size: 15px;
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
  padding: 24px;
  font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace;
  font-size: 14px;
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
  font-size: 15px;
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
