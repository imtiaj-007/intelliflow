import axiosClient from '@/lib/axios'
import { AxiosError } from 'axios'

export interface UploadDocument {
    file_name: string
    file_size: number
    file_ext: string
    mime_type: string
    workflow_id: string
}

export interface UploadDocumentResponse {
    id: string
    url: string
    file_key: string
    mime_type: string
    expires_in: number
}

export interface APIResponse<T> {
    data: T | null
    status?: number
    message?: string
    error?: string
}

export const FileService = {
    getUploadURL: async (
        doc_data: UploadDocument
    ): Promise<APIResponse<UploadDocumentResponse>> => {
        try {
            const res = await axiosClient.post('/file/upload', doc_data)
            return res
        } catch (error) {
            return {
                status: error instanceof AxiosError ? error.status : 500,
                data: null,
                error: `Failed to get upload URL`,
            }
        }
    },
    uploadFileToAWS: async (upload_url: string, file: File): Promise<boolean> => {
        try {
            const res = await fetch(upload_url, {
                method: 'PUT',
                body: file,
                headers: {
                    'Content-Type': file.type,
                    'Content-Length': file.size.toString(),
                },
                credentials: 'omit', // Don't send cookies to AWS S3
            })

            if (!res.ok) {
                throw new Error(`AWS upload failed with status: ${res.status}`)
            }
            return true
        } catch (error) {
            return false
        }
    },
    processDocument: async (
        file_id: string,
        workflow_id: string
    ): Promise<APIResponse<unknown>> => {
        try {
            const res = await axiosClient.post(`/file/${file_id}/process`, { workflow_id })
            return res
        } catch (error) {
            return {
                status: error instanceof AxiosError ? error.status : 500,
                data: null,
                error: `Failed to process document: ${file_id}`,
            }
        }
    },
}
