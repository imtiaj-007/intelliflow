import { Field, FieldContent, FieldLabel } from '@/components/ui/field'
import { Textarea } from '@/components/ui/textarea'
import { Node, NodeProps } from '@xyflow/react'
import { MessageSquare } from 'lucide-react'
import { memo, useState } from 'react'
import { BaseNode, BaseNodeData } from './base'

export interface UserQueryNodeData extends BaseNodeData {
    query?: string
}

export type UserQueryNodeType = Node<UserQueryNodeData, 'UserQuery'>

export const UserQueryNode = memo(({ data, ...props }: NodeProps<UserQueryNodeType>) => {
    const [query, setQuery] = useState(data.query || '')

    return (
        <BaseNode
            data={{
                ...data,
                label: 'User Query',
                icon: <MessageSquare className='w-5 h-5 text-orange-500' />,
                description: 'Entry point for querys',
            }}
            showTargetHandle={false}
            {...props}>
            <Field orientation='vertical'>
                <FieldLabel className='text-xs'>User Query</FieldLabel>
                <FieldContent>
                    <Textarea
                        placeholder='Write your query here'
                        value={query}
                        onChange={e => setQuery(e.target.value)}
                        className='text-sm resize-none'
                    />
                </FieldContent>
            </Field>
        </BaseNode>
    )
})

UserQueryNode.displayName = 'UserQueryNode'
