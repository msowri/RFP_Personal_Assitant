export function showToast(message: string, type: 'success' | 'error' = 'error') {

  const bgClass = type === 'success'
    ? 'text-bg-success'
    : 'text-bg-danger'

  const toast = document.createElement('div')
  toast.className = `toast align-items-center ${bgClass} show position-fixed bottom-0 end-0 m-3`

  toast.innerHTML = `
    <div class="d-flex">
      <div class="toast-body">${message}</div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto"></button>
    </div>
  `

  document.body.appendChild(toast)

  // Close button
  toast.querySelector('.btn-close')?.addEventListener('click', () => {
    toast.remove()
  })

  setTimeout(() => {
    toast.remove()
  }, 3000)
}
