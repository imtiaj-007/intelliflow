import { Field, FieldContent, FieldLabel } from '@/components/ui/field'
import { Node, NodeProps } from '@xyflow/react'
import { FileOutput } from 'lucide-react'
import { memo } from 'react'
import { BaseNode, BaseNodeData } from './base'

export interface OutputNodeData extends BaseNodeData {
    outputText?: string
}

export type OutputNodeType = Node<OutputNodeData, 'OutputNode'>

export const OutputNode = memo(({ data, ...props }: NodeProps<OutputNodeType>) => {
    return (
        <BaseNode
            data={{
                ...data,
                label: 'Output',
                icon: <FileOutput className='w-5 h-5 text-purple-500' />,
                description: 'Output of the result nodes as text',
            }}
            showSourceHandle={false}
            {...props}>
            <div className='space-y-3'>
                <Field orientation='vertical'>
                    <FieldLabel className='text-xs'>Output Text</FieldLabel>
                    <FieldContent>
                        <div className='min-h-[80px] p-3 rounded-md bg-gray-50 border text-sm text-gray-500'>
                            {data.outputText || 'Output will be generated based on query'}
                        </div>
                    </FieldContent>
                </Field>
            </div>
        </BaseNode>
    )
})

OutputNode.displayName = 'OutputNode'
