<script setup>
import { ref, onMounted } from 'vue'
import PageHeader from '@/components/shared/PageHeader.vue'
import StatusBadge from '@/components/shared/StatusBadge.vue'
import { Button } from '@/components/ui/button'
import { getApiKeyStatus, setApiKey, removeApiKey } from '@/api/settingsApi'

const isKeySet = ref(false)
const apiKeyInput = ref('')
const loading = ref(false)
const message = ref('')
const messageType = ref('') // 'success' | 'error'

async function loadStatus() {
  try {
    const data = await getApiKeyStatus()
    isKeySet.value = data.is_set
  } catch (e) {
    // Silently fail — settings endpoint might not exist yet
  }
}

async function handleSave() {
  if (!apiKeyInput.value.trim()) return
  loading.value = true
  message.value = ''
  try {
    await setApiKey(apiKeyInput.value.trim())
    apiKeyInput.value = '' // Clear immediately — never retain
    message.value = 'API key saved successfully.'
    messageType.value = 'success'
    await loadStatus()
  } catch (e) {
    message.value = e.message
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}

async function handleRemove() {
  loading.value = true
  message.value = ''
  try {
    await removeApiKey()
    message.value = 'API key removed.'
    messageType.value = 'success'
    await loadStatus()
  } catch (e) {
    message.value = e.message
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}

onMounted(loadStatus)
</script>

<template>
  <div class="view">
    <PageHeader
      title="Settings"
      subtitle="Application configuration and API keys"
    />

    <div class="settings-body">
      <section class="settings-card">
        <div class="settings-card__header">
          <h2 class="settings-card__title">Anthropic API Key</h2>
          <p class="settings-card__desc">
            Required for RAG-powered query answering in the Regulatory Assistant.
          </p>
        </div>

        <div class="settings-card__status">
          <StatusBadge v-if="isKeySet" status="pass" />
          <StatusBadge v-else status="warning" />
          <span class="settings-card__status-label">
            <template v-if="isKeySet">
              Configured &mdash; Your API key is saved. Enter a new key below to replace it.
            </template>
            <template v-else>
              Not configured &mdash; An Anthropic API key is required for the Regulatory Assistant.
            </template>
          </span>
        </div>

        <div class="settings-card__form">
          <label class="form-label" for="api-key-input">API Key</label>
          <input
            id="api-key-input"
            v-model="apiKeyInput"
            type="password"
            class="form-input"
            placeholder="sk-ant-..."
            :disabled="loading"
            @keyup.enter="handleSave"
          />
          <div class="form-actions">
            <Button
              :disabled="loading || !apiKeyInput.trim()"
              @click="handleSave"
            >
              {{ loading ? 'Saving...' : 'Save Key' }}
            </Button>
            <Button
              v-if="isKeySet"
              variant="destructive"
              :disabled="loading"
              @click="handleRemove"
            >
              {{ loading ? 'Removing...' : 'Remove Key' }}
            </Button>
          </div>
        </div>

        <!-- Success / error message -->
        <div
          v-if="message"
          class="settings-card__message"
          :class="{
            'settings-card__message--success': messageType === 'success',
            'settings-card__message--error': messageType === 'error',
          }"
        >
          {{ message }}
        </div>

        <p class="settings-card__note">
          The key is stored locally in the database and is never displayed after saving.
          It is used only for RAG query answering in the Regulatory Assistant.
        </p>
      </section>
    </div>
  </div>
</template>

<style scoped>
.view {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.settings-body {
  flex: 1;
  overflow-y: auto;
  padding: 28px;
}

.settings-card {
  max-width: 640px;
  background-color: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.settings-card__header {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.settings-card__title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.settings-card__desc {
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.5;
}

.settings-card__status {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  background-color: var(--bg-surface-2);
  border-radius: 6px;
}

.settings-card__status-label {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.4;
}

.settings-card__form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.form-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.form-input {
  height: 38px;
  padding: 0 12px;
  border-radius: 6px;
  border: 1px solid var(--border-subtle);
  background-color: var(--bg-surface-2);
  color: var(--text-primary);
  font-size: 14px;
  font-family: inherit;
  outline: none;
  transition: border-color 0.15s ease;
}

.form-input::placeholder {
  color: var(--text-muted);
}

.form-input:focus {
  border-color: var(--border-strong);
}

.form-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-actions {
  display: flex;
  gap: 8px;
  padding-top: 4px;
}

.settings-card__message {
  font-size: 13px;
  padding: 10px 14px;
  border-radius: 6px;
  line-height: 1.4;
}

.settings-card__message--success {
  background-color: color-mix(in srgb, var(--color-success) 10%, transparent);
  color: var(--color-success);
}

.settings-card__message--error {
  background-color: color-mix(in srgb, var(--color-danger) 10%, transparent);
  color: var(--color-danger);
}

.settings-card__note {
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.5;
  border-top: 1px solid var(--border-subtle);
  padding-top: 16px;
}
</style>
