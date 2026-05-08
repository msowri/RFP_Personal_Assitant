<template>
  <div>
    <div v-if="documents.length === 0" class="text-muted">
      No documents uploaded yet.
    </div>

    <div v-else>
      <div class="table-responsive">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>File Name</th>
              <th>Type</th>
              <th>Size</th>
              <th>Uploaded</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="doc in documents" :key="doc.id">
              <td>{{ doc.file_name }}</td>
              <td>
                <span class="badge bg-secondary">{{ doc.file_type.toUpperCase() }}</span>
              </td>
              <td>{{ formatFileSize(doc.file_size) }}</td>
              <td>{{ formatDate(doc.created_on) }}</td>
              <td>
                <button class="btn btn-sm btn-outline-primary" @click="selectDocument(doc)">
                  Query
                </button>
                <button class="btn btn-sm btn-outline-danger" @click="deleteDocument(doc)">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRfpStore } from '../stores/useRfpStore'
import httpHandler from '../services/httphandler'
import { showToast } from '../utils/apptoaster'

const rfpStore = useRfpStore()

const documents = computed(() => rfpStore.documents)

function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString()
}

async function selectDocument(doc: any) {
  rfpStore.setSelectedDocument(doc)
  await rfpStore.loadDocumentQuestions(doc.id)
  showToast(`Selected ${doc.file_name} for questioning`, 'info')
}

async function deleteDocument(doc: any) {
  if (!confirm(`Are you sure you want to delete ${doc.file_name}?`)) {
    return
  }

  try {
    await httpHandler.delete(`/documents/${doc.id}`)
    await rfpStore.loadDocuments()
    showToast('Document deleted successfully', 'success')
  } catch (error) {
    console.error('Failed to delete document:', error)
    showToast('Failed to delete document', 'error')
  }
}

onMounted(async () => {
  await rfpStore.loadDocuments()
})
</script>
