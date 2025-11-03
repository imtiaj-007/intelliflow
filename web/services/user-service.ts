import axiosClient from '@/lib/axios'
import { AxiosError } from 'axios'

export interface APIResponse<T> {
    data: T | null
    status?: number
    message?: string
    error?: string
}

export const UserService = {
    getUserProfile: async (): Promise<APIResponse<{ success: boolean; message: string }>> => {
        try {
            const res = await axiosClient.get(`/user`)
            return res
        } catch (error) {
            return {
                status: error instanceof AxiosError ? error.status : 500,
                data: null,
                error: 'Failed to get user profile',
            }
        }
    },
}
