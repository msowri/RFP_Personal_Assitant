<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h4>RFP Personal Assistant</h4>
        <p class="text-muted">Upload documents, extract questions, generate answers, and export responses.</p>
      </div>
    </div>

    <div class="row g-4">
      <div class="col-lg-4">
        <FileUpload />
        <QuestionExtraction />
      </div>

      <div class="col-lg-8">
        <div class="row g-4">
          <div class="col-12">
            <QueryInterface />
          </div>

          <div class="col-12">
            <DocumentList />
          </div>

          <div class="col-12">
            <DraftManager />
          </div>

          <div class="col-12">
            <ExportInterface />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import FileUpload from '../components/FileUpload.vue'
import QueryInterface from '../components/QueryInterface.vue'
import DocumentList from '../components/DocumentList.vue'
import ExportInterface from '../components/ExportInterface.vue'
import QuestionExtraction from '../components/QuestionExtraction.vue'
import DraftManager from '../components/DraftManager.vue'
</script>
