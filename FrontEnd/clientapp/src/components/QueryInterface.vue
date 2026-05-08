<template>
  <div>
    <div class="mb-3">
      <label for="query" class="form-label">Ask a Question:</label>
      <textarea
        id="query"
        class="form-control"
        v-model="query"
        rows="3"
        placeholder="Enter your question about the uploaded documents..."
      ></textarea>
    </div>
    <div v-if="selectedDocument" class="alert alert-secondary">
      Querying against: <strong>{{ selectedDocument.file_name }}</strong>
    </div>

    <button class="btn btn-primary" @click="submitQuery" :disabled="isLoading">
      {{ isLoading ? 'Processing...' : 'Ask Question' }}
    </button>

    <div v-if="answer" class="mt-3">
      <h6>Answer:</h6>
      <div class="alert alert-info">
        {{ answer }}
      </div>
    </div>

    <div v-if="error" class="mt-3">
      <div class="alert alert-danger">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRfpStore } from '../stores/useRfpStore'
import { showToast } from '../utils/apptoaster'

const rfpStore = useRfpStore()
const query = ref('')
const error = ref('')
const isLoading = ref(false)

const selectedDocument = computed(() => rfpStore.selectedDocument)
const answer = computed(() => rfpStore.answer)

async function submitQuery() {
  if (!query.value.trim()) {
    showToast('Please enter a question', 'error')
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    await rfpStore.queryDocument(query.value, 5, selectedDocument.value?.id)
    showToast('Query processed successfully', 'success')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to process query'
    showToast('Query failed', 'error')
  } finally {
    isLoading.value = false
  }
}
</script>
