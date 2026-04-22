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
import httpHandler from '../services/httphandler'
import { showToast } from '../utils/apptoaster'

const file = ref<File | null>(null)

const allowedTypes = [
  'application/pdf',
  'text/plain',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document' //Latest format
]

const maxSize = 5 * 1024 * 1024 // 5MB

function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement

  if (!input.files || input.files.length === 0) return

  const selectedFile = input.files[0]

  // File type validation
  if (selectedFile && !allowedTypes.includes(selectedFile.type)) {
    showToast("Only PDF, DOC,DOCX & TXT allowed")
    return
  }

  if (selectedFile && selectedFile.size > maxSize) {
    showToast("File size must be less than 5MB")
    return
  }
  // if (selectedFile) {
  //   showToast("File selected: " + selectedFile.name)
  // }
  if (selectedFile) {
    file.value = selectedFile
  }
}

async function uploadFile() {

  if (!file.value) {
    showToast("Please select a file")
    return
  }

  const formData = new FormData()
  formData.append('file', file.value)

  try {
    await httpHandler.post('/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    showToast("File uploaded successfully", "success")

  } catch (error) {
    showToast("Upload failed", "error")
  }
}

</script>
