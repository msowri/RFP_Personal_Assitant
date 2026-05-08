<template>
  <div class="card mb-4">
    <div class="card-header">
      <h5>Extract Questions</h5>
    </div>
    <div class="card-body">
      <div class="mb-3">
        <label class="form-label">Select Document</label>
        <select class="form-select" v-model.number="selectedDocumentId">
          <option :value="null">Use raw text</option>
          <option v-for="doc in documents" :key="doc.id" :value="doc.id">
            {{ doc.file_name }}
          </option>
        </select>
      </div>

      <div class="mb-3">
        <label class="form-label">Or paste text to extract questions</label>
        <textarea class="form-control" v-model="rawText" rows="4" placeholder="Paste document text here..."></textarea>
      </div>

      <div class="d-flex gap-2 mb-3">
        <button class="btn btn-primary" @click="extractQuestions" :disabled="isLoading">
          {{ isLoading ? 'Extracting...' : 'Extract Questions' }}
        </button>
        <button class="btn btn-outline-secondary" @click="clearForm">Clear</button>
      </div>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <div v-if="questions.length">
        <h6>Extracted Questions</h6>
        <ul class="list-group mb-3">
          <li class="list-group-item d-flex justify-content-between align-items-start" v-for="question in questions" :key="question">
            <div>{{ question }}</div>
            <button class="btn btn-sm btn-outline-success" @click="createDraft(question)">Save Draft</button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRfpStore } from '../stores/useRfpStore'
import { showToast } from '../utils/apptoaster'

const rfpStore = useRfpStore()
const rawText = ref('')
const selectedDocumentId = ref<number | null>(null)
const error = ref('')
const isLoading = ref(false)
const questions = ref<string[]>([])

const documents = computed(() => rfpStore.documents)

onMounted(async () => {
  if (!rfpStore.documents.length) {
    await rfpStore.loadDocuments()
  }
})

async function extractQuestions() {
  if (!selectedDocumentId.value && !rawText.value.trim()) {
    showToast('Select a document or paste text first.', 'error')
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    const payload = {
      document_id: selectedDocumentId.value ?? undefined,
      text: rawText.value.trim() || undefined,
      store: true
    }
    const response = await rfpStore.extractQuestions(payload.document_id, payload.text, payload.store)
    questions.value = response.questions || []
    showToast(`Extracted ${questions.value.length} questions`, 'success')
  } catch (err) {
    error.value = 'Failed to extract questions.'
    showToast('Question extraction failed', 'error')
  } finally {
    isLoading.value = false
  }
}

async function createDraft(question: string) {
  try {
    await rfpStore.createDraft(question, '', selectedDocumentId.value ?? undefined)
    showToast('Draft created from question', 'success')
    await rfpStore.loadDrafts()
  } catch (err) {
    showToast('Unable to save draft', 'error')
  }
}

function clearForm() {
  selectedDocumentId.value = null
  rawText.value = ''
  questions.value = []
  error.value = ''
}
</script>
