import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle } from '@/components/ui/card'
import { cn } from '@/lib/utils'
import { Handle, NodeProps, Position } from '@xyflow/react'
import { Settings } from 'lucide-react'
import { memo, ReactNode } from 'react'

export interface BaseNodeData {
    label: string
    icon?: ReactNode
    variant?: 'default' | 'primary' | 'secondary'
    description?: string
    [key: string]: unknown
}

export interface BaseNodeProps extends NodeProps {
    data: BaseNodeData
    children?: ReactNode
    showSourceHandle?: boolean
    showTargetHandle?: boolean
    multiSource?: boolean
    onSettingsClick?: () => void
}

export const BaseNode = memo(
    ({
        data,
        children,
        showSourceHandle = true,
        showTargetHandle = true,
        onSettingsClick = () => {},
        selected,
    }: BaseNodeProps) => {
        return (
            <Card
                className={cn(
                    'w-80 p-0 gap-0 shadow-md transition-all',
                    selected && 'ring-2 ring-blue-500'
                )}>
                {showTargetHandle && (
                    <Handle
                        type='target'
                        position={Position.Left}
                        className='size-3! bg-gray-400! border-2! border-white!'
                    />
                )}

                <CardHeader className='pt-3 border-b'>
                    <CardTitle className='flex items-center gap-2'>
                        {data.icon && (
                            <div className='shrink-0 w-5 h-5 flex items-center justify-center'>
                                {data.icon}
                            </div>
                        )}
                        <h3 className='font-semibold text-base truncate'>{data.label}</h3>
                        {onSettingsClick && (
                            <Button
                                variant='ghost'
                                size='icon'
                                className='h-6 w-6 shrink-0 ml-auto'
                                onClick={onSettingsClick}>
                                <Settings className='h-3.5 w-3.5' />
                            </Button>
                        )}
                    </CardTitle>
                </CardHeader>
                <p className='text-xs font-medium text-gray-600 bg-blue-50 px-6 py-2 rounded'>
                    {data.description}
                </p>

                {children && <div className='p-4'>{children}</div>}

                {showSourceHandle && (
                    <Handle
                        type='source'
                        position={Position.Right}
                        className='size-3! bg-gray-400! border-2! border-white!'
                    />
                )}
            </Card>
        )
    }
)

BaseNode.displayName = 'BaseNode'
