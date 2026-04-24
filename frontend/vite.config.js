import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const railwayFrontendHost = 'frontend-web-production-6d53.up.railway.app'
const extraAllowedHost = process.env.VITE_ALLOWED_HOST

const allowedHosts = [railwayFrontendHost]
if (extraAllowedHost) {
  allowedHosts.push(extraAllowedHost)
}

export default defineConfig({
  plugins: [react()],
  preview: {
    allowedHosts
  }
})
