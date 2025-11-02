import { useDnD } from '@/context/DnDContext'
import { BookOpen, Brain, Code, MessageSquare } from 'lucide-react'

const nodeConfig = [
    { type: 'userQuery', label: 'User Query', icon: MessageSquare },
    { type: 'knowledgeBase', label: 'Knowledge Base', icon: BookOpen },
    { type: 'llm', label: 'LLM', icon: Brain },
    { type: 'output', label: 'Output', icon: Code },
]

export const NodeOptions: React.FC = () => {
    const [_, setType] = useDnD()

    const onDragStart = (event: React.DragEvent<HTMLDivElement>, nodeType: string) => {
        setType(nodeType)
        event.dataTransfer.effectAllowed = 'move'
    }

    const onDragEnd = () => {
        setType(null)
    }

    return (
        <div className='flex flex-col gap-2'>
            {nodeConfig.map(node => (
                <div
                    key={node.type}
                    data-node-type={node.type}
                    draggable
                    onDragStart={e => onDragStart(e, node.type)}
                    onDragEnd={onDragEnd}
                    className='p-2 border rounded-sm cursor-move hover:bg-gray-50 transition-colors'>
                    <div className='flex items-center gap-2'>
                        <node.icon className='size-4' />
                        <span className='text-sm font-medium'>{node.label}</span>
                    </div>
                </div>
            ))}
        </div>
    )
}
