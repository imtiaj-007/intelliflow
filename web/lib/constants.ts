import { Brain, LucideIcon } from 'lucide-react'

export interface ModelOption {
    label: string
    value: string
    icon?: LucideIcon
}

export const embeddingModels: ModelOption[] = [
    // OpenAI models
    { label: 'text-embedding-3-large', value: 'text-embedding-3-large', icon: Brain },
    { label: 'text-embedding-3-small', value: 'text-embedding-3-small', icon: Brain },
    { label: 'text-embedding-ada-002', value: 'text-embedding-ada-002', icon: Brain },

    // Google AI models
    { label: 'gemini-embedding-001', value: 'gemini-embedding-001', icon: Brain },
    { label: 'text-embedding-005', value: 'text-embedding-005', icon: Brain },
    {
        label: 'text-multilingual-embedding-002',
        value: 'text-multilingual-embedding-002',
        icon: Brain,
    },

    // Anthropic models
    { label: 'voyage-3-large', value: 'voyage-3-large', icon: Brain },
    { label: 'voyage-3.5', value: 'voyage-3.5', icon: Brain },
    { label: 'voyage-3.5-lite', value: 'voyage-3.5-lite', icon: Brain },
]

export const llmModels: ModelOption[] = [
    // OpenAI models
    { label: 'GPT-5', value: 'gpt-5', icon: Brain },
    { label: 'GPT-4.1', value: 'gpt-4.1', icon: Brain },
    { label: 'GPT-4.1 Turbo', value: 'gpt-4.1-turbo', icon: Brain },
    { label: 'GPT-4o', value: 'gpt-4o', icon: Brain },

    // Anthropic models
    { label: 'Claude Opus-4.1', value: 'claude-4-1-opus-20240229', icon: Brain },
    { label: 'Claude Sonnet-4.5', value: 'claude-4-5-sonnet-20240620', icon: Brain },
    { label: 'Claude Haiku-4.5', value: 'claude-4-5-haiku-20240307', icon: Brain },
    { label: 'Claude Sonnet-3.7', value: 'claude-3-7-sonnet-20240229', icon: Brain },

    // Google AI models
    { label: 'Gemini 2.5 Pro', value: 'gemini-2.5-pro', icon: Brain },
    { label: 'Gemini 2.5 Flash', value: 'gemini-2.5-flash', icon: Brain },
    { label: 'Gemini 2.5 Flash Lite', value: 'gemini-2.5-flash-lite', icon: Brain },
    { label: 'Gemini 2.0 Flash', value: 'gemini-2.0-flash', icon: Brain },
]
