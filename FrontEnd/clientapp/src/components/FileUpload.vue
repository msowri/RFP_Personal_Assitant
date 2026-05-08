<template>
  <div class="container mt-4">

    <input type="file" class="form-control" @change="onFileChange" />

    <button class="btn btn-primary mt-3" @click="uploadFile">
      Upload
    </button>

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRfpStore } from '../stores/useRfpStore'
import httpHandler from '../services/httphandler'
import { showToast } from '../utils/apptoaster'

const file = ref<File | null>(null)
const isLoading = ref(false)
const error = ref('')
const rfpStore = useRfpStore()

const allowedTypes = [
  'application/pdf',
  'text/plain',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
]

const maxSize = 50 * 1024 * 1024 // 50MB

function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  if (!input.files || input.files.length === 0) return

  const selectedFile = input.files[0]
  if (!selectedFile) return

  if (!allowedTypes.includes(selectedFile.type)) {
    showToast('Only PDF, DOC, DOCX & TXT allowed', 'error')
    return
  }

  if (selectedFile.size > maxSize) {
    showToast('File size must be less than 50MB', 'error')
    return
  }

  file.value = selectedFile
}

async function uploadFile() {
  if (!file.value) {
    showToast('Please select a file before uploading', 'error')
    return
  }

  isLoading.value = true
  error.value = ''

  const formData = new FormData()
  formData.append('file', file.value)

  try {
    const response = await httpHandler.post('/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    showToast(`Uploaded ${response.data.file_name} successfully`, 'success')
    file.value = null
    await rfpStore.loadDocuments()
    await rfpStore.loadDrafts()
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Upload failed. Please try again.'
    showToast(error.value, 'error')
  } finally {
    isLoading.value = false
  }
}
</script>
