'use client'

import ChatCanvas from '@/components/chat/ChatCanvas'
import { Button } from '@/components/ui/button'
import { Spinner } from '@/components/ui/spinner'
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'
import { useApp } from '@/context/AppContext'
import { useDnD } from '@/context/DnDContext'
import {
    Background,
    Connection,
    ControlButton,
    Controls,
    Edge,
    MiniMap,
    Node,
    ReactFlow,
    ReactFlowProvider,
    XYPosition,
    addEdge,
    useEdgesState,
    useNodesState,
    useReactFlow,
    useViewport,
} from '@xyflow/react'
import { MessageCircleMoreIcon, PlayIcon } from 'lucide-react'
import { useCallback, useEffect, useRef } from 'react'
import { nodeTypes } from './nodes/types'

function CustomControls() {
    const { zoom } = useViewport()
    const zoomPercentage = Math.round(zoom * 100)

    return (
        <Controls
            position='bottom-center'
            orientation='horizontal'
            showInteractive={false}>
            <ControlButton>{zoomPercentage}%</ControlButton>
        </Controls>
    )
}

const initialNodes: Node[] = []
const initialEdges: Edge[] = []

function DnDFlow({ workflowId }: { workflowId: string }) {
    const reactFlowWrapper = useRef<HTMLDivElement>(null)
    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes)
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges)
    const { screenToFlowPosition } = useReactFlow()
    const [type] = useDnD()
    const { workflow, workflowStatus, processFile, loading } = useApp()

    useEffect(() => {
        workflow[1]({
            title: '',
            description: '',
            id: workflowId,
        })
    }, [workflowId])

    const onConnect = useCallback(
        (params: Connection) => setEdges(eds => addEdge(params, eds)),
        [setEdges]
    )

    const onDragOver = useCallback((event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault()
        event.dataTransfer.dropEffect = 'move'
    }, [])

    const getId = () => `node-${Date.now()}`

    const onDrop = useCallback(
        (event: React.DragEvent<HTMLDivElement>) => {
            event.preventDefault()
            if (!type) {
                return
            }

            const position: XYPosition = screenToFlowPosition({
                x: event.clientX,
                y: event.clientY,
            })

            const newNode: Node = {
                id: getId(),
                type,
                position,
                data: { label: `${type} node` },
            }

            setNodes(nds => [...(nds as Node[]), newNode])
        },
        [screenToFlowPosition, type, setNodes]
    )

    return (
        <div
            style={{ width: '100%', height: '100%', position: 'relative' }}
            ref={reactFlowWrapper}>
            <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                onDrop={onDrop}
                onDragOver={onDragOver}
                nodeTypes={nodeTypes}
                nodesDraggable={true}
                fitView>
                <Background />
                <CustomControls />
                <MiniMap
                    zoomable
                    pannable
                    position='bottom-left'
                    nodeStrokeWidth={3}
                    nodeColor={node => {
                        switch (node.type) {
                            case 'userQuery':
                                return '#fb923c'
                            case 'knowledgeBase':
                                return '#3b82f6'
                            case 'llm':
                                return '#10b981'
                            case 'output':
                                return '#a855f7'
                            default:
                                return '#e2e8f0'
                        }
                    }}
                />
            </ReactFlow>
            <div className='absolute bottom-8 right-4 flex flex-col gap-3'>
                <Tooltip>
                    <TooltipTrigger>
                        <Button
                            size='icon-lg'
                            className='rounded-full'
                            onClick={processFile}>
                            {loading.processing ? (
                                <Spinner />
                            ) : (
                                <PlayIcon
                                    className='size-5'
                                    fill='white'
                                />
                            )}
                        </Button>
                    </TooltipTrigger>
                    <TooltipContent side='left'>Build Workflow</TooltipContent>
                </Tooltip>
                <Tooltip>
                    <TooltipTrigger>
                        <ChatCanvas>
                            <Button
                                variant='primary'
                                size='icon-lg'
                                className='rounded-full'>
                                <MessageCircleMoreIcon
                                    className='size-5'
                                    fill='white'
                                />
                            </Button>
                        </ChatCanvas>
                    </TooltipTrigger>
                    <TooltipContent side='left'>Run Workflow</TooltipContent>
                </Tooltip>
            </div>
        </div>
    )
}

interface FlowCanvasProps {
    workflowId: string
}

const FlowCanvas: React.FC<FlowCanvasProps> = ({ workflowId }) => {
    return (
        <ReactFlowProvider>
            <DnDFlow workflowId={workflowId} />
        </ReactFlowProvider>
    )
}

export default FlowCanvas
