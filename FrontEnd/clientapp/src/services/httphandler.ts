import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api' // Ffeature move to .env

const httpHandler  = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

httpHandler.interceptors.request.use(config => {
  return config
})

httpHandler.interceptors.response.use(
  response => response,
  error => {
    console.error("API Error:", error)
    return Promise.reject(error)
  }
)

export default httpHandler
