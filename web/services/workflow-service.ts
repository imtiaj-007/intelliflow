import axiosClient from '@/lib/axios'
import { AxiosError } from 'axios'

export interface CreateWorkflow {
    title: string
    description: string
}

export interface WorkflowResponse {
    id: string
    user_id: string
    name: string
    description: string
    is_active: boolean
    created_at: string
    updated_at: string
}
export interface PaginatedResponse<T> {
    data: T[]
    current_page: number
    total_pages: number
    total_records: number
}

export interface APIResponse<T> {
    data: T | null
    status?: number
    message?: string
    error?: string
}

export const WorkflowService = {
    createWorkflow: async (data: CreateWorkflow): Promise<APIResponse<WorkflowResponse>> => {
        try {
            const res = await axiosClient.post('/workflow', data)
            return res
        } catch (error) {
            return {
                status: error instanceof AxiosError ? error.status : 500,
                data: null,
                error: 'Failed to create workflow',
            }
        }
    },
    getWorkflows: async (
        page: number = 1,
        limit: number = 20
    ): Promise<APIResponse<PaginatedResponse<WorkflowResponse>>> => {
        try {
            const params = new URLSearchParams({
                page: page.toString(),
                limit: limit.toString(),
            })
            const res = await axiosClient.get(`/workflow?${params}`)
            return res
        } catch (error) {
            return {
                status: error instanceof AxiosError ? error.status : 500,
                data: null,
                error: 'Failed to get workflows',
            }
        }
    },
    chatWithWorkflow: async (workflow_id: string, query: string): Promise<APIResponse<string>> => {
        try {
            const res = await axiosClient.post(`/workflow/${workflow_id}/chat`, { query })
            return res
        } catch (error) {
            return {
                status: error instanceof AxiosError ? error.status : 500,
                data: null,
                error: 'Failed to get workflows',
            }
        }
    },
}
