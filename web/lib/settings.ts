type EnvType = 'development' | 'production'

export interface AppSettings {
    ENV: EnvType
    DEFAULT_PAGE: number
    DEFAULT_PAGE_LIMIT: number
    MAX_RECONNECT_ATTEMPTS: number
    RECONNECT_DELAY: number

    API_KEY: string
    SECRET_KEY: string

    FRONTEND_URL: string
    LOGO_URL: string

    GOOGLE_TAG: string
    GOOGLE_VERIFICATION_CODE: string

    BACKEND_URL: string
    API_BASE_URL: string
}

export const settings: AppSettings = {
    ENV: (process.env.NEXT_PUBLIC_ENV as EnvType) || 'development',
    DEFAULT_PAGE: 1,
    DEFAULT_PAGE_LIMIT: 10,

    MAX_RECONNECT_ATTEMPTS: 3,
    RECONNECT_DELAY: 5000,

    API_KEY: process.env.NEXT_PUBLIC_API_KEY || 'your-api-key',
    SECRET_KEY: process.env.NEXT_PUBLIC_SECRET_KEY || 'your-secret-key',

    FRONTEND_URL: process.env.NEXT_PUBLIC_FRONTEND_URL || 'http://localhost:3000',
    LOGO_URL: process.env.NEXT_PUBLIC_LOGO_URL || 'http://localhost:3000/logo.png',

    GOOGLE_TAG: process.env.NEXT_PUBLIC_GTAG_ID || 'your-g-tag',
    GOOGLE_VERIFICATION_CODE:
        process.env.NEXT_PUBLIC_GOOGLE_VERIFICATION_CODE || 'your-verification-code',

    BACKEND_URL: process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000',
    API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1',
}
