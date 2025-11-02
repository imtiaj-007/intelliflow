import { Button } from '@/components/ui/button'
import { Field, FieldContent, FieldLabel } from '@/components/ui/field'
import { Input } from '@/components/ui/input'
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select'
import { embeddingModels } from '@/lib/constants'
import { Node, NodeProps } from '@xyflow/react'
import { BookOpen, Eye, EyeOff, Upload } from 'lucide-react'
import { memo, useState } from 'react'
import { BaseNode, BaseNodeData } from './base'

export interface KnowledgeBaseNodeData extends BaseNodeData {
    embeddingModel?: string
    apiKey?: string
    fileName?: string
}

export type KnowledgeBaseNodeType = Node<KnowledgeBaseNodeData, 'knowledgeBase'>

export const KnowledgeBaseNode = memo(({ data, ...props }: NodeProps<KnowledgeBaseNodeType>) => {
    const [embeddingModel, setEmbeddingModel] = useState(
        data.embeddingModel || 'text-embedding-3-large'
    )
    const [apiKey, setApiKey] = useState(data.apiKey || '')
    const [showApiKey, setShowApiKey] = useState(false)
    const [fileName, setFileName] = useState(data.fileName || '')

    const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0]
        if (file) {
            setFileName(file.name)
        }
    }

    return (
        <BaseNode
            data={{
                ...data,
                label: 'Knowledge Base',
                icon: <BookOpen className='w-5 h-5 text-blue-500' />,
                description: 'Let LLM search info in your file',
            }}
            {...props}>
            <div className='space-y-4'>
                <Field orientation='vertical'>
                    <FieldLabel className='text-xs'>File for Knowledge Base</FieldLabel>
                    <FieldContent>
                        <div className='border-2 border-dashed rounded-lg p-4 text-center'>
                            <input
                                type='file'
                                id='file-upload'
                                className='hidden'
                                onChange={handleFileUpload}
                            />
                            <label
                                htmlFor='file-upload'
                                className='cursor-pointer'>
                                <Upload className='w-6 h-6 mx-auto text-gray-400 mb-2' />
                                <span className='text-sm text-blue-600'>Upload File</span>
                            </label>
                            {fileName && <p className='text-xs text-gray-600 mt-2'>{fileName}</p>}
                        </div>
                    </FieldContent>
                </Field>

                <Field orientation='vertical'>
                    <FieldLabel className='text-xs'>Embedding Model</FieldLabel>
                    <FieldContent>
                        <Select
                            value={embeddingModel}
                            onValueChange={setEmbeddingModel}>
                            <SelectTrigger className='w-full'>
                                <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                                {embeddingModels.map(model => (
                                    <SelectItem
                                        key={model.value}
                                        value={model.value}>
                                        {model.label}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </FieldContent>
                </Field>

                <Field orientation='vertical'>
                    <FieldLabel className='text-xs'>API Key</FieldLabel>
                    <FieldContent>
                        <div className='relative'>
                            <Input
                                type={showApiKey ? 'text' : 'password'}
                                value={apiKey}
                                onChange={e => setApiKey(e.target.value)}
                                placeholder='******************'
                                className='pr-10'
                            />
                            <Button
                                variant='ghost'
                                size='icon'
                                className='absolute right-0 top-0 h-full'
                                onClick={() => setShowApiKey(!showApiKey)}>
                                {showApiKey ? (
                                    <EyeOff className='h-4 w-4' />
                                ) : (
                                    <Eye className='h-4 w-4' />
                                )}
                            </Button>
                        </div>
                    </FieldContent>
                </Field>
            </div>
        </BaseNode>
    )
})

KnowledgeBaseNode.displayName = 'KnowledgeBaseNode'
