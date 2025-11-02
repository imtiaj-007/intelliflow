import { KnowledgeBaseNode } from '@/components/flow-builder/nodes/KnowledgeBase'
import { LLMNode } from '@/components/flow-builder/nodes/LLM'
import { OutputNode } from '@/components/flow-builder/nodes/Output'
import { UserQueryNode } from '@/components/flow-builder/nodes/UserQuery'

export const nodeTypes = {
    userQuery: UserQueryNode,
    knowledgeBase: KnowledgeBaseNode,
    llm: LLMNode,
    output: OutputNode,
}

export type NodeType = keyof typeof nodeTypes
