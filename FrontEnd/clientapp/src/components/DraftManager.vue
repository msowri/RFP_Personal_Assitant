<template>
  <div class="card mb-4">
    <div class="card-header">
      <h5>Draft Manager</h5>
    </div>
    <div class="card-body">
      <div v-if="drafts.length === 0" class="text-muted">
        No drafts available. Upload documents or extract questions to create drafts.
      </div>

      <div v-else>
        <div v-for="draft in drafts" :key="draft.id" class="card mb-3">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <strong>Q:</strong> {{ draft.question }}
              </div>
              <button class="btn btn-sm btn-danger" @click="removeDraft(draft.id)">Delete</button>
            </div>

            <div class="mb-3">
              <label class="form-label">Answer</label>
              <textarea
                class="form-control"
                rows="4"
                v-model="editedAnswers[draft.id]"
                @input="markEdited(draft.id)"
              ></textarea>
            </div>

            <div class="d-flex gap-2">
              <button class="btn btn-sm btn-primary" @click="saveDraft(draft)">Save</button>
              <span class="badge" :class="draft.is_edited ? 'bg-success' : 'bg-secondary'">
                {{ draft.is_edited ? 'Edited' : 'Generated' }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRfpStore } from '../stores/useRfpStore'
import { showToast } from '../utils/apptoaster'

const rfpStore = useRfpStore()
const editedAnswers = ref<Record<number, string>>({})
const error = ref('')

const drafts = computed(() => rfpStore.drafts)

onMounted(async () => {
  if (!rfpStore.drafts.length) {
    await rfpStore.loadDrafts()
  }
})

watch(
  drafts,
  (newDrafts) => {
    newDrafts.forEach((draft) => {
      editedAnswers.value[draft.id] = draft.answer || ''
    })
  },
  { immediate: true }
)

function markEdited(draftId: number) {
  if (!(draftId in editedAnswers.value)) {
    editedAnswers.value[draftId] = ''
  }
}

async function saveDraft(draft: any) {
  error.value = ''
  try {
    await rfpStore.updateDraft(draft.id, {
      answer: editedAnswers.value[draft.id],
      is_edited: true
    })
    showToast('Draft saved successfully', 'success')
    await rfpStore.loadDrafts()
  } catch (err) {
    error.value = 'Unable to save draft.'
    showToast('Save failed', 'error')
  }
}

async function removeDraft(draftId: number) {
  if (!confirm('Delete this draft?')) {
    return
  }
  try {
    await rfpStore.deleteDraft(draftId)
    showToast('Draft deleted', 'success')
  } catch (err) {
    error.value = 'Unable to delete draft.'
    showToast('Delete failed', 'error')
  }
}
</script>
