import { defineStore } from 'pinia'
import httpHandler from '../services/httphandler'

export interface DocumentItem {
  id: number
  file_name: string
  file_type: string
  file_size: number
  created_on: string
  updated_on?: string
}

export interface DraftItem {
  id: number
  question: string
  answer: string
  document_id?: number
  is_edited: boolean
  created_on: string
  updated_on: string
}

export interface QuestionItem {
  id: number
  question_text: string
  normalized_text?: string
  is_extracted: boolean
  created_on: string
}

export const useRfpStore = defineStore('rfp', {
  state: () => ({
    documents: [] as DocumentItem[],
    drafts: [] as DraftItem[],
    questions: [] as QuestionItem[],
    selectedDocument: null as DocumentItem | null,
    selectedQuestion: null as QuestionItem | null,
    answer: '',
    error: '',
    loading: false
  }),

  actions: {
    async loadDocuments(limit = 20, offset = 0) {
      this.loading = true
      try {
        const response = await httpHandler.get('/documents/', { params: { limit, offset } })
        this.documents = response.data.documents || response.data || []
      } catch (err) {
        console.error('Error loading documents', err)
        this.error = 'Unable to load documents.'
      } finally {
        this.loading = false
      }
    },

    async loadDrafts() {
      this.loading = true
      try {
        const response = await httpHandler.get('/drafts/')
        this.drafts = response.data || []
      } catch (err) {
        console.error('Error loading drafts', err)
        this.error = 'Unable to load drafts.'
      } finally {
        this.loading = false
      }
    },

    async loadDocumentQuestions(documentId: number) {
      this.loading = true
      try {
        const response = await httpHandler.get(`/questions/document/${documentId}`)
        this.questions = response.data.questions || []
      } catch (err) {
        console.error('Error loading document questions', err)
        this.error = 'Unable to load questions for document.'
      } finally {
        this.loading = false
      }
    },

    setSelectedDocument(document: DocumentItem | null) {
      this.selectedDocument = document
    },

    async createDraft(question: string, answer: string, document_id?: number) {
      this.loading = true
      try {
        const response = await httpHandler.post('/drafts/', {
          question,
          answer,
          document_id
        })
        this.drafts.unshift(response.data)
        return response.data
      } catch (err) {
        console.error('Error creating draft', err)
        this.error = 'Unable to save draft.'
        throw err
      } finally {
        this.loading = false
      }
    },

    async updateDraft(draftId: number, payload: { question?: string; answer?: string; is_edited?: boolean }) {
      this.loading = true
      try {
        const response = await httpHandler.put(`/drafts/${draftId}`, payload)
        const updated = response.data
        const index = this.drafts.findIndex((draft) => draft.id === updated.id)
        if (index >= 0) {
          this.drafts[index] = updated
        }
        return updated
      } catch (err) {
        console.error('Error updating draft', err)
        this.error = 'Unable to update draft.'
        throw err
      } finally {
        this.loading = false
      }
    },

    async deleteDraft(draftId: number) {
      this.loading = true
      try {
        await httpHandler.delete(`/drafts/${draftId}`)
        this.drafts = this.drafts.filter((draft) => draft.id !== draftId)
      } catch (err) {
        console.error('Error deleting draft', err)
        this.error = 'Unable to delete draft.'
        throw err
      } finally {
        this.loading = false
      }
    },

    async extractQuestions(documentId?: number, text?: string, store = false) {
      this.loading = true
      try {
        const response = await httpHandler.post('/questions/extract', {
          document_id: documentId,
          text,
          store
        })
        return response.data
      } catch (err) {
        console.error('Error extracting questions', err)
        this.error = 'Unable to extract questions.'
        throw err
      } finally {
        this.loading = false
      }
    },

    async queryDocument(query: string, top_k = 5, document_id?: number) {
      this.loading = true
      try {
        const response = await httpHandler.post('/query/', {
          query,
          top_k,
          document_id
        })
        this.answer = response.data.answer
        return response.data
      } catch (err) {
        console.error('Error querying document', err)
        this.error = 'Unable to query document.'
        throw err
      } finally {
        this.loading = false
      }
    }
  }
})
