import { KnowledgeBaseForm } from '@/forms/KnowledgeBaseFom'
import { Node, NodeProps } from '@xyflow/react'
import { BookOpen } from 'lucide-react'
import { memo } from 'react'
import { BaseNode, BaseNodeData } from './base'

export interface KnowledgeBaseNodeData extends BaseNodeData {
    embeddingModel?: string
    apiKey?: string
    fileName?: string
}

export type KnowledgeBaseNodeType = Node<KnowledgeBaseNodeData, 'knowledgeBase'>

export const KnowledgeBaseNode = memo(({ data, ...props }: NodeProps<KnowledgeBaseNodeType>) => {
    return (
        <BaseNode
            data={{
                ...data,
                label: 'Knowledge Base',
                icon: <BookOpen className='w-5 h-5 text-blue-500' />,
                description: 'Let LLM search info in your file',
            }}
            {...props}>
            <KnowledgeBaseForm />
        </BaseNode>
    )
})

KnowledgeBaseNode.displayName = 'KnowledgeBaseNode'
