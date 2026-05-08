# RFP Personal Assistant - Input/Output Examples

## File Upload Examples

### Input: File Upload Request
```
Method: POST
Endpoint: /api/files/upload
Content-Type: multipart/form-data

Form Data:
- file: [binary file data]
```

### Output: Successful Upload Response
```json
{
  "success": true,
  "file_id": "uuid-1234-5678-9012",
  "file_name": "Sample_IT_Services_RFP.txt",
  "file_size_mb": 0.045,
  "file_type": "txt",
  "document_id": 123,
  "chunks_created": 28,
  "total_characters": 8750
}
```

### Output: Upload Error Response
```json
{
  "detail": "File exceeds 50MB limit"
}
```

---

## Question Extraction Examples

### Input: Extract Questions from Document
```
Method: POST
Endpoint: /api/questions/extract
Content-Type: application/json

{
  "document_id": 123
}
```

### Output: Question Extraction Response
```json
{
  "questions": [
    "What is your company's experience with enterprise-scale cloud infrastructure modernization?",
    "How do you ensure data security and compliance during migration processes?",
    "Can you provide examples of similar projects completed in the last 3 years?",
    "What is your typical implementation timeline for a project of this scale?",
    "How do you handle change management and user training?",
    "What are your pricing models for ongoing support and maintenance?",
    "How do you ensure minimal downtime during migration?",
    "What certifications does your company currently hold?",
    "Can you provide client references from similar projects?",
    "What is your approach to legacy system integration?",
    "What are your SLA guarantees for post-migration support?",
    "How do you handle scope changes and additional requirements?"
  ],
  "total_questions": 12,
  "source": "Document ID: 123"
}
```

---

## Query Examples

### Input: Document Query
```
Method: POST
Endpoint: /api/query/
Content-Type: application/json

{
  "query": "What are the security requirements for this project?",
  "top_k": 5,
  "document_id": null
}
```

### Output: Query Response
```json
{
  "answer": "Based on the RFP document, the security requirements include:\n\n• ISO 27001:2013 certification mandatory\n• SOC 2 Type II compliance required\n• End-to-end encryption for all data transmission\n• Multi-factor authentication implementation\n• Regular security audits and penetration testing\n• GDPR compliance for European operations\n• HIPAA compliance for healthcare data handling\n\nThe client specifically requires providers with proven security frameworks and recent audit reports.",
  "relevant_chunks": [
    "Security and Compliance\n- ISO 27001:2013 certification mandatory\n- SOC 2 Type II compliance required\n- End-to-end encryption for all data transmission",
    "Multi-factor authentication implementation\n- Regular security audits and penetration testing\n- GDPR compliance for European operations",
    "HIPAA compliance for healthcare data handling\n- Provider must demonstrate expertise in enterprise-scale cloud deployments"
  ]
}
```

---

## Draft Management Examples

### Input: Create Draft
```
Method: POST
Endpoint: /drafts/
Content-Type: application/json

{
  "question": "What is your company's experience with enterprise-scale cloud infrastructure modernization?",
  "answer": "Our company has 15 years of experience in cloud infrastructure, having successfully deployed over 200 enterprise solutions across AWS, Azure, and Google Cloud platforms.",
  "document_id": 123,
  "is_edited": false
}
```

### Output: Draft Creation Response
```json
{
  "id": 456,
  "question": "What is your company's experience with enterprise-scale cloud infrastructure modernization?",
  "answer": "Our company has 15 years of experience in cloud infrastructure, having successfully deployed over 200 enterprise solutions across AWS, Azure, and Google Cloud platforms.",
  "document_id": 123,
  "is_edited": false,
  "created_on": "2024-05-08T10:30:00Z",
  "updated_on": "2024-05-08T10:30:00Z"
}
```

### Input: Update Draft
```
Method: PUT
Endpoint: /drafts/456
Content-Type: application/json

{
  "answer": "Our company has 15 years of experience in cloud infrastructure, having successfully deployed over 200 enterprise solutions across AWS, Azure, and Google Cloud platforms. We specialize in scalable, secure cloud architectures that support mission-critical operations.\n\nRecent relevant projects include:\n- Fortune 500 financial services firm (2023) - Migrated 50TB data to AWS\n- Healthcare provider (2022) - Built HIPAA-compliant Azure infrastructure\n- E-commerce platform (2023) - Designed auto-scaling architecture handling 1M+ daily users",
  "is_edited": true
}
```

---

## Export Examples

### Input: Export Drafts
```
Method: POST
Endpoint: /api/export/drafts
Content-Type: application/json

{
  "draft_ids": [456, 457, 458],
  "format": "docx",
  "include_metadata": true
}
```

### Output: Export Response
```
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
Content-Disposition: attachment; filename=rfp_export_2024-05-08.docx
Content-Length: 45678

[Binary DOCX file content]
```

### Input: Export Q&A Pairs
```
Method: POST
Endpoint: /api/export/qa
Content-Type: application/json

{
  "qa_pairs": [
    {
      "question": "What is your company's experience with enterprise-scale cloud infrastructure modernization?",
      "answer": "Our company has 15 years of experience..."
    },
    {
      "question": "How do you ensure data security and compliance during migration processes?",
      "answer": "Our security framework includes..."
    }
  ],
  "title": "RFP Response - ABC Corporation",
  "format": "docx",
  "metadata": {
    "client": "ABC Corporation",
    "project": "IT Infrastructure Modernization",
    "submission_date": "2024-06-15"
  }
}
```

---

## Document Management Examples

### Input: List Documents
```
Method: GET
Endpoint: /api/documents/?limit=10&offset=0
```

### Output: Document List Response
```json
{
  "success": true,
  "documents": [
    {
      "id": 123,
      "file_name": "Sample_IT_Services_RFP.txt",
      "file_type": "txt",
      "file_size": 46080,
      "created_on": "2024-05-08T10:30:00Z",
      "updated_on": "2024-05-08T10:30:00Z",
      "has_content": true
    },
    {
      "id": 124,
      "file_name": "Technical_Requirements.pdf",
      "file_type": "pdf",
      "file_size": 2621440,
      "created_on": "2024-05-08T09:15:00Z",
      "updated_on": "2024-05-08T09:15:00Z",
      "has_content": true
    }
  ],
  "total": 2,
  "limit": 10,
  "offset": 0
}
```

### Input: Get Document Details
```
Method: GET
Endpoint: /api/documents/123
```

### Output: Document Details Response
```json
{
  "id": 123,
  "file_name": "Sample_IT_Services_RFP.txt",
  "file_type": "txt",
  "file_size": 46080,
  "created_on": "2024-05-08T10:30:00Z",
  "updated_on": "2024-05-08T10:30:00Z",
  "has_content": true,
  "chunks_count": 28
}
```

---

## Health Check Examples

### Input: Health Check
```
Method: GET
Endpoint: /health
```

### Output: Health Check Response
```json
{
  "status": "healthy",
  "app": "RFP Personal Assistant"
}
```

---

## Error Response Examples

### Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "query"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Not Found Error
```json
{
  "detail": "Document not found"
}
```

### Processing Error
```json
{
  "detail": "Text extraction failed: Unsupported file type"
}
```

### Database Error
```json
{
  "detail": "Database connection failed"
}
```

---

## File Processing Examples

### Input: Text Extraction Only
```
Method: POST
Endpoint: /api/files/extract-text
Content-Type: multipart/form-data

Form Data:
- file: [binary file data]
```

### Output: Text Extraction Response
```json
{
  "success": true,
  "file_name": "Sample_IT_Services_RFP.txt",
  "file_type": "txt",
  "file_size_mb": 0.045,
  "characters_extracted": 8750,
  "text": "REQUEST FOR PROPOSAL\nIT Infrastructure Modernization Project\n\nRFP-2024-015\nIssue Date: May 8, 2024\nDue Date: June 15, 2024\n\n1. PROJECT OVERVIEW\nABC Corporation is requesting proposals..."
}
```

### Input: File Validation
```
Method: GET
Endpoint: /api/files/validate/Sample_IT_Services_RFP.txt/46080
```

### Output: Validation Response
```json
{
  "valid": true,
  "message": "Valid",
  "filename": "Sample_IT_Services_RFP.txt",
  "file_size_mb": 0.045,
  "max_allowed_mb": 50,
  "allowed_types": ["pdf", "txt", "docx"]
}
```

---

## Frontend Component Examples

### File Upload Component State
```javascript
// Initial state
{
  selectedFile: null,
  isUploading: false,
  uploadProgress: 0,
  errorMessage: ''
}

// After file selection
{
  selectedFile: {
    name: 'Sample_IT_Services_RFP.txt',
    size: 46080,
    type: 'text/plain'
  },
  isUploading: false,
  uploadProgress: 0,
  errorMessage: ''
}

// During upload
{
  selectedFile: { /* file object */ },
  isUploading: true,
  uploadProgress: 65,
  errorMessage: ''
}

// After successful upload
{
  selectedFile: null,
  isUploading: false,
  uploadProgress: 100,
  errorMessage: '',
  uploadResult: {
    success: true,
    documentId: 123,
    fileName: 'Sample_IT_Services_RFP.txt'
  }
}
```

### Query Component State
```javascript
// Before query
{
  query: 'What are the security requirements?',
  isProcessing: false,
  answer: '',
  errorMessage: ''
}

// During processing
{
  query: 'What are the security requirements?',
  isProcessing: true,
  answer: '',
  errorMessage: ''
}

// After successful query
{
  query: 'What are the security requirements?',
  isProcessing: false,
  answer: 'Based on the RFP document, the security requirements include...',
  errorMessage: ''
}
```

### Export Component State
```javascript
// Export configuration
{
  format: 'docx',
  includeMetadata: true,
  exportOption: 'all',
  selectedDrafts: [],
  isExporting: false,
  errorMessage: ''
}

// During export
{
  format: 'docx',
  includeMetadata: true,
  exportOption: 'all',
  selectedDrafts: [],
  isExporting: true,
  errorMessage: '',
  exportProgress: 45
}

// After successful export
{
  format: 'docx',
  includeMetadata: true,
  exportOption: 'all',
  selectedDrafts: [],
  isExporting: false,
  errorMessage: '',
  downloadUrl: 'blob:http://localhost:3000/abc123-def456'
}
```

---

## API Response Format Standards

### Success Response Format
```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Operation completed successfully"
}
```

### Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": { /* error details */ }
  }
}
```

### Pagination Response Format
```json
{
  "success": true,
  "data": [ /* array of items */ ],
  "pagination": {
    "total": 150,
    "limit": 10,
    "offset": 0,
    "has_next": true,
    "has_prev": false
  }
}
```

---

## Testing Data Examples

### Sample Document Content for Testing
```
REQUEST FOR PROPOSAL
Software Development Services

1. REQUIREMENTS
- Web application development using React
- Mobile app for iOS and Android
- REST API integration
- Database design and implementation

2. TECHNICAL SPECIFICATIONS
- Frontend: React, TypeScript, Tailwind CSS
- Backend: Node.js, Express, PostgreSQL
- Mobile: React Native
- DevOps: Docker, Kubernetes, AWS

3. PROJECT TIMELINE
- Phase 1: Requirements gathering (2 weeks)
- Phase 2: Development (12 weeks)
- Phase 3: Testing (4 weeks)
- Phase 4: Deployment (2 weeks)

4. QUESTIONS
1. What is your experience with React development?
2. Can you provide examples of mobile apps you've built?
3. How do you ensure code quality and testing?
4. What is your approach to project management?
5. What are your pricing models?
```

### Expected Query Results
```
Query: "What technologies are required for frontend development?"
Expected Answer: "Based on the document, frontend technologies required are React, TypeScript, and Tailwind CSS."

Query: "How long is the development phase?"
Expected Answer: "The development phase is scheduled for 12 weeks according to the project timeline."
```

These examples provide comprehensive coverage of all input/output scenarios for testing and development purposes.
