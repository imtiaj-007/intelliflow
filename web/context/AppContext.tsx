'use client'

import { FileService, UploadDocumentResponse } from '@/services/file-service'
import { WorkflowService } from '@/services/workflow-service'
import { createContext, ReactNode, useContext, useState } from 'react'
import { toast } from 'sonner'

interface FileState extends UploadDocumentResponse {
    file: File
}

interface WorkflowState {
    title: string
    description: string
    id: string
}

interface ChatState {
    role: 'user' | 'assistant'
    message: string
}

interface AppContextType {
    workflow: [WorkflowState | undefined, (workflow: WorkflowState | undefined) => void]
    fileState: FileState | undefined
    workflowStatus: 'uploaded' | 'processed' | 'failed' | undefined
    chatState: ChatState[]
    loading: {
        uploading: boolean
        processing: boolean
        chatting: boolean
    }
    uploadFile: (file: File) => Promise<void>
    processFile: () => Promise<void>
    chatWithWorkflow: (query: string) => void
}

const AppContext = createContext<AppContextType>({
    workflow: [undefined, () => {}],
    fileState: undefined,
    workflowStatus: undefined,
    chatState: [],
    loading: {
        uploading: false,
        processing: false,
        chatting: false,
    },
    uploadFile: async () => {},
    processFile: async () => {},
    chatWithWorkflow: async () => undefined,
})

interface AppProviderProps {
    children: ReactNode
}

export const AppProvider = ({ children }: AppProviderProps) => {
    const [workflow, setWorkflow] = useState<WorkflowState>()
    const [workflowStatus, setWorkflowStatus] = useState<'uploaded' | 'processed' | 'failed'>()
    const [fileState, setFileState] = useState<FileState>()
    const [chatState, setChatState] = useState<ChatState[]>([])
    const [loading, setLoading] = useState({
        uploading: false,
        processing: false,
        chatting: false,
    })

    const uploadFile = async (file: File) => {
        if (!file || !workflow?.id) return
        try {
            setLoading(prev => ({ ...prev, uploading: true }))
            const urlRes = await FileService.getUploadURL({
                file_name: file.name,
                file_size: file.size,
                file_ext: file.name.split('.').pop() || '',
                mime_type: file.type,
                workflow_id: workflow?.id,
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
        if (!fileState || !fileState.id || !workflow?.id) return
        try {
            setLoading(prev => ({ ...prev, processing: true }))
            const res = await FileService.processDocument(fileState.id, workflow?.id)
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

    const chatWithWorkflow = async (query: string) => {
        if (!workflow?.id) return
        try {
            setLoading(prev => ({ ...prev, chatting: true }))
            setChatState(prev => [{ role: 'user', message: query }, ...prev])
            const res = await WorkflowService.chatWithWorkflow(workflow.id, query)
            if (res.data) {
                setChatState(prev => [
                    {
                        role: 'assistant',
                        message:
                            res.data ??
                            'Sorry, I was unable to generate a response. This could be due to a network issue or insufficient document context.',
                    },
                    ...prev,
                ])
            }
        } catch (error) {
            toast.error('Failed to chat with workflow')
        } finally {
            setLoading(prev => ({ ...prev, chatting: false }))
        }
    }

    return (
        <AppContext.Provider
            value={{
                workflow: [workflow, setWorkflow],
                fileState: fileState,
                workflowStatus: workflowStatus,
                chatState: chatState,
                loading,
                uploadFile,
                processFile,
                chatWithWorkflow,
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
