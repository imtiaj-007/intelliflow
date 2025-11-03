'use client'

import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import {
    InputGroup,
    InputGroupAddon,
    InputGroupButton,
    InputGroupText,
    InputGroupTextarea,
} from '@/components/ui/input-group'
import { useApp } from '@/context/AppContext'
import { cn } from '@/lib/utils'
import { ArrowUpIcon, BrainCircuit, Plus, Scale, ToolCase } from 'lucide-react'
import { useState } from 'react'

interface ChatboxProps {
    className?: string
}

const Chatbox: React.FC<ChatboxProps> = ({ className }) => {
    const [message, setMessage] = useState('')
    const { chatWithWorkflow, loading } = useApp()

    const handleSendMessage = async () => {
        const msg = message.trim()
        if (msg) {
            chatWithWorkflow(msg)
            setMessage('')
        }
    }

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSendMessage()
        }
    }

    return (
        <div className={cn(className)}>
            <InputGroup>
                <InputGroupTextarea
                    placeholder='Ask, Search or Chat...'
                    value={message}
                    onChange={e => setMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                />
                <InputGroupAddon align='block-end'>
                    <InputGroupButton
                        variant='outline'
                        className='rounded-full'
                        size='icon-xs'>
                        <Plus />
                    </InputGroupButton>
                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <InputGroupButton variant='ghost'>Auto</InputGroupButton>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent
                            side='top'
                            align='start'
                            className='[--radius:0.95rem]'>
                            <DropdownMenuItem>
                                <Scale /> Auto
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                                <BrainCircuit /> Agent
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                                <ToolCase /> Manual
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                    <InputGroupText className='ml-auto text-xs'>52% used</InputGroupText>
                    <InputGroupButton
                        variant='default'
                        className='rounded-full'
                        size='icon-xs'
                        onClick={handleSendMessage}
                        disabled={!message.trim() || loading.chatting}>
                        <ArrowUpIcon />
                        <span className='sr-only'>Send</span>
                    </InputGroupButton>
                </InputGroupAddon>
            </InputGroup>
        </div>
    )
}

export default Chatbox
