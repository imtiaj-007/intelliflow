'use client'

import { FileService, UploadDocumentResponse } from '@/services/file-service'
import { createContext, ReactNode, useContext, useState } from 'react'
import { toast } from 'sonner'

interface FileState extends UploadDocumentResponse {
    file: File
}

interface WorkflowState {
    title: string
    description: string
}

interface AppContextType {
    workflow: WorkflowState | undefined
    fileState: FileState | undefined
    workflowStatus: 'uploaded' | 'processed' | 'failed' | undefined
    loading: {
        uploading: boolean
        processing: boolean
    }
    uploadFile: (file: File) => Promise<void>
    processFile: () => Promise<void>
}

const AppContext = createContext<AppContextType>({
    workflow: undefined,
    fileState: undefined,
    workflowStatus: undefined,
    loading: {
        uploading: false,
        processing: false,
    },
    uploadFile: async () => {},
    processFile: async () => {},
})

interface AppProviderProps {
    children: ReactNode
}

export const AppProvider = ({ children }: AppProviderProps) => {
    const [workflow, setWorkflow] = useState<WorkflowState>()
    const [workflowStatus, setWorkflowStatus] = useState<'uploaded' | 'processed' | 'failed'>()
    const [fileState, setFileState] = useState<FileState>()
    const [loading, setLoading] = useState({
        uploading: false,
        processing: false,
    })

    const uploadFile = async (file: File) => {
        if (!file) return
        try {
            setLoading(prev => ({ ...prev, uploading: true }))
            const urlRes = await FileService.getUploadURL({
                file_name: file.name,
                file_size: file.size,
                file_ext: file.name.split('.').pop() || '',
                mime_type: file.type,
            })
            if (urlRes && urlRes.data) {
                const uploadRes = await FileService.uploadFileToAWS(urlRes.data.url, file)
                if (uploadRes) {
                    const newFileState = {
                        ...urlRes.data,
                        file: file,
                    }
                    setFileState(newFileState)
                    setWorkflowStatus('uploaded')
                    toast.success('File Uploaded Successfully')
                }
            }
        } catch (error) {
            toast.error('Failed to Upload File')
        } finally {
            setWorkflowStatus('failed')
            setLoading(prev => ({ ...prev, uploading: false }))
        }
    }

    const processFile = async () => {
        if (!fileState || !fileState.id) return
        try {
            setLoading(prev => ({ ...prev, processing: true }))
            const res = await FileService.processDocument(fileState.id)
            if (res.data) {
                setWorkflowStatus('processed')
                toast.success('File Processed Successfully')
            }
        } catch (error) {
            toast.error('Failed to Process File')
        } finally {
            setWorkflowStatus('failed')
            setLoading(prev => ({ ...prev, processing: false }))
        }
    }

    return (
        <AppContext.Provider
            value={{
                workflow: workflow,
                fileState: fileState,
                workflowStatus: workflowStatus,
                loading,
                uploadFile,
                processFile,
            }}>
            {children}
        </AppContext.Provider>
    )
}

export default AppContext

export const useApp = (): AppContextType => {
    return useContext(AppContext)
}

export const useWorkflow = () => {
    const { workflow, workflowStatus } = useApp()
    return { workflow, workflowStatus }
}

export const useFileState = () => {
    const { fileState, loading } = useApp()
    return { fileState, loading }
}

export const useFileActions = () => {
    const { uploadFile, processFile, loading } = useApp()
    return { uploadFile, processFile, loading }
}
