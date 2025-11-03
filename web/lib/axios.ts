import { settings } from '@/lib/settings'
import axios from 'axios'

const axiosClient = axios.create({
    baseURL: settings.API_BASE_URL || 'http://localhost:8000/api/v1',
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true,
})

// Request interceptor
axiosClient.interceptors.request.use(
    config => {
        // Add timezone header
        const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone
        config.headers['x-timezone'] = timezone

        // Add screen resolution header
        if (typeof window !== 'undefined') {
            const screenResolution = `${window.screen.width}x${window.screen.height}`
            config.headers['x-screen-resolution'] = screenResolution
        }

        return config
    },
    error => {
        return Promise.reject(error)
    }
)

// Response interceptor
axiosClient.interceptors.response.use(
    response => {
        return response
    },
    error => {
        if (error.response?.status === 401 && typeof window !== 'undefined') {
            window.location.href = '/login'
        }
        return Promise.reject(error)
    }
)

export default axiosClient
