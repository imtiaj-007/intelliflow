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
import { Switch } from '@/components/ui/switch'
import { Textarea } from '@/components/ui/textarea'
import { llmModels } from '@/lib/constants'
import { Node, NodeProps } from '@xyflow/react'
import { Brain, Eye, EyeOff } from 'lucide-react'
import { memo, useState } from 'react'
import { BaseNode, BaseNodeData } from './base'

export interface LLMNodeData extends BaseNodeData {
    model?: string
    apiKey?: string
    serfApiKey?: string
    prompt?: string
    temperature?: number
    webSearchEnabled?: boolean
}

export type LLMNodeType = Node<LLMNodeData, 'LLMNode'>

export const LLMNode = memo(({ data, ...props }: NodeProps<LLMNodeType>) => {
    const [model, setModel] = useState(data.model || 'gpt-5')
    const [apiKey, setApiKey] = useState(data.apiKey || '')
    const [serfApiKey, setSerfApiKey] = useState(data.serfApiKey || '')
    const [showApiKey, setShowApiKey] = useState(false)
    const [showSerfKey, setShowSerfKey] = useState(false)
    const [prompt, setPrompt] = useState<string>(data.prompt || '')
    const [temperature, setTemperature] = useState<number>(data.temperature || 0.75)
    const [webSearchEnabled, setWebSearchEnabled] = useState<boolean>(data.webSearchEnabled || true)

    return (
        <BaseNode
            data={{
                ...data,
                label: 'LLM (OpenAI)',
                icon: <Brain className='w-5 h-5 text-green-500' />,
                description: 'Run a query with OpenAI LLM',
            }}
            {...props}>
            <div className='space-y-3'>
                <Field orientation='vertical'>
                    <FieldLabel className='text-xs'>Model</FieldLabel>
                    <FieldContent>
                        <Select
                            value={model}
                            onValueChange={setModel}>
                            <SelectTrigger className='w-full'>
                                <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                                {llmModels.map(model => (
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

                <Field orientation='vertical'>
                    <FieldLabel className='text-xs'>Prompt</FieldLabel>
                    <FieldContent>
                        <Textarea
                            value={prompt}
                            onChange={e => setPrompt(e.target.value)}
                            placeholder='You are a helpful PDF assistant. Use web search if the PDF lacks context'
                            className='min-h-[80px] text-sm resize-none'
                        />
                    </FieldContent>
                </Field>

                <Field orientation='vertical'>
                    <FieldLabel className='text-xs'>Temperature</FieldLabel>
                    <FieldContent>
                        <div className='flex items-center gap-2'>
                            <Input
                                type='number'
                                value={temperature}
                                onChange={e => setTemperature(parseFloat(e.target.value))}
                                min='0'
                                max='2'
                                step='0.1'
                                className='flex-1'
                            />
                        </div>
                    </FieldContent>
                </Field>

                <div className='flex items center justify-between border-b py-2'>
                    <span className='text-sm font-medium'>WebSearch Tool</span>
                    <Switch
                        id='2fa'
                        className='data-[state=checked]:bg-green-500'
                        onCheckedChange={(checked: boolean) => setWebSearchEnabled(checked)}
                    />
                </div>

                {webSearchEnabled && (
                    <Field orientation='vertical'>
                        <FieldLabel className='text-xs'>SERF API</FieldLabel>
                        <FieldContent>
                            <div className='relative'>
                                <Input
                                    type={showSerfKey ? 'text' : 'password'}
                                    value={serfApiKey}
                                    onChange={e => setSerfApiKey(e.target.value)}
                                    placeholder='******************'
                                    className='pr-10'
                                />
                                <Button
                                    variant='ghost'
                                    size='icon'
                                    className='absolute right-0 top-0 h-full'
                                    onClick={() => setShowSerfKey(!showSerfKey)}>
                                    {showSerfKey ? (
                                        <EyeOff className='h-4 w-4' />
                                    ) : (
                                        <Eye className='h-4 w-4' />
                                    )}
                                </Button>
                            </div>
                        </FieldContent>
                    </Field>
                )}
            </div>
        </BaseNode>
    )
})

LLMNode.displayName = 'LLMNode'
