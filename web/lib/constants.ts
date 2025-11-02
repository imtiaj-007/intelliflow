import { Brain, LucideIcon } from 'lucide-react'

export interface ModelOption {
    label: string
    value: string
    icon?: LucideIcon
}

export const embeddingModels: ModelOption[] = [
    // OpenAI models
    { label: 'text-embedding-3-small', value: 'text-embedding-3-small', icon: Brain },
    { label: 'text-embedding-3-large', value: 'text-embedding-3-large', icon: Brain },
    { label: 'text-embedding-ada-002', value: 'text-embedding-ada-002', icon: Brain },

    // Google AI models
    { label: 'text-embedding-004', value: 'text-embedding-004', icon: Brain },
    {
        label: 'text-multilingual-embedding-002',
        value: 'text-multilingual-embedding-002',
        icon: Brain,
    },
    { label: 'text-embedding-preview-0409', value: 'text-embedding-preview-0409', icon: Brain },

    // Anthropic models
    { label: 'claude-3-sonnet-embedding', value: 'claude-3-sonnet-embedding', icon: Brain },
    { label: 'claude-3-opus-embedding', value: 'claude-3-opus-embedding', icon: Brain },
    { label: 'claude-3-haiku-embedding', value: 'claude-3-haiku-embedding', icon: Brain },
]

export const llmModels: ModelOption[] = [
    // OpenAI models
    { label: 'GPT-5', value: 'gpt-5', icon: Brain },
    { label: 'GPT-4.1', value: 'gpt-4.1', icon: Brain },
    { label: 'GPT-4.1-turbo', value: 'gpt-4.1-turbo', icon: Brain },
    { label: 'GPT-3.5-turbo', value: 'gpt-3.5-turbo', icon: Brain },

    // Anthropic models
    { label: 'Claude 4.5 Sonnet', value: 'claude-3-5-sonnet-20240620', icon: Brain },
    { label: 'Claude 4.1 Sonnet', value: 'claude-3-sonnet-20240229', icon: Brain },
    { label: 'Claude 4.1 Opus', value: 'claude-3-opus-20240229', icon: Brain },
    { label: 'Claude 4.1 Haiku', value: 'claude-3-haiku-20240307', icon: Brain },

    // Google AI models
    { label: 'Gemini 2.5 Pro', value: 'gemini-2.5-pro', icon: Brain },
    { label: 'Gemini 2.5 Flash', value: 'gemini-2.5-flash', icon: Brain },
    { label: 'Gemini 2.0 Pro', value: 'gemini-2.0-pro', icon: Brain },
    { label: 'Gemini 2.0 Flash', value: 'gemini-2.0-flash', icon: Brain },
]
