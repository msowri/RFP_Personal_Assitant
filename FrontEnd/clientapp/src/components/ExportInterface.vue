<template>
  <div class="card">
    <div class="card-header">
      <h5>Export Responses</h5>
    </div>
    <div class="card-body">
      <div class="mb-3">
        <label for="exportFormat" class="form-label">Export Format:</label>
        <select id="exportFormat" class="form-select" v-model="exportFormat">
          <option value="docx">Word Document (.docx)</option>
          <option value="txt">Plain Text (.txt)</option>
        </select>
      </div>
      
      <div class="mb-3">
        <div class="form-check">
          <input class="form-check-input" type="checkbox" v-model="includeMetadata" id="includeMetadata">
          <label class="form-check-label" for="includeMetadata">
            Include document metadata
          </label>
        </div>
      </div>
      
      <div class="mb-3">
        <label class="form-label">Export Options:</label>
        <div class="btn-group w-100" role="group">
          <input type="radio" class="btn-check" name="exportOption" id="exportAll" value="all" v-model="exportOption">
          <label class="btn btn-outline-primary" for="exportAll">All Drafts</label>
          
          <input type="radio" class="btn-check" name="exportOption" id="exportSelected" value="selected" v-model="exportOption">
          <label class="btn btn-outline-primary" for="exportSelected">Selected Drafts</label>
          
          <input type="radio" class="btn-check" name="exportOption" id="exportQA" value="qa" v-model="exportOption">
          <label class="btn btn-outline-primary" for="exportQA">Q&A Only</label>
        </div>
      </div>
      
      <div v-if="exportOption === 'selected'" class="mb-3">
        <label class="form-label">Select drafts to export:</label>
        <div class="border p-2 rounded" style="max-height: 200px; overflow-y: auto;">
          <div v-for="draft in drafts" :key="draft.id" class="form-check">
            <input class="form-check-input" type="checkbox" :value="draft.id" v-model="selectedDrafts" :id="'draft-' + draft.id">
            <label class="form-check-label" :for="'draft-' + draft.id">
              {{ draft.question?.substring(0, 50) }}...
            </label>
          </div>
        </div>
      </div>
      
      <button class="btn btn-success" @click="exportData" :disabled="isLoading || !canExport">
        {{ isLoading ? 'Exporting...' : 'Export' }}
      </button>
      
      <div v-if="error" class="mt-3">
        <div class="alert alert-danger">
          {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import httpHandler from '../services/httphandler'
import { showToast } from '../utils/apptoaster'

interface Draft {
  id: number
  question: string
  answer: string
  is_edited: boolean
  created_on: string
}

const exportFormat = ref('docx')
const includeMetadata = ref(true)
const exportOption = ref('all')
const selectedDrafts = ref<number[]>([])
const drafts = ref<Draft[]>([])
const isLoading = ref(false)
const error = ref('')

const canExport = computed(() => {
  if (exportOption.value === 'selected') {
    return selectedDrafts.value.length > 0
  }
  return true
})

async function loadDrafts() {
  try {
    const response = await httpHandler.get('/drafts/')
    drafts.value = response.data
  } catch (err) {
    console.error('Failed to load drafts:', err)
  }
}

async function exportData() {
  isLoading.value = true
  error.value = ''
  
  try {
    let exportData: any = {
      format: exportFormat.value,
      include_metadata: includeMetadata.value
    }
    
    if (exportOption.value === 'selected') {
      exportData.draft_ids = selectedDrafts.value
    }
    
    const response = await httpHandler.post('/export/drafts', exportData, {
      responseType: 'blob'
    })
    
    // Create download link
    const blob = new Blob([response.data])
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    
    const filename = `rfp_export_${new Date().toISOString().split('T')[0]}.${exportFormat.value}`
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    showToast('Export completed successfully', 'success')
    
  } catch (err: any) {
    error.value = 'Export failed. Please try again.'
    showToast('Export failed', 'error')
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadDrafts()
})
</script>
