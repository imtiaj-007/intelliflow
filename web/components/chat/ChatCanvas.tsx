'use client'

import Chatbox from '@/components/chat/ChatBox'
import MarkdownViewer from '@/components/chat/MarkdownViewer'
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet'
import { Thinker } from '@/components/ui/spinner'
import { useApp } from '@/context/AppContext'
import { cn } from '@/lib/utils'
import { ReactNode } from 'react'

interface ChatCanvasProps {
    children: ReactNode
}

const ChatCanvas: React.FC<ChatCanvasProps> = ({ children }) => {
    const { chatState, loading } = useApp()

    return (
        <Sheet>
            <SheetTrigger asChild>{children}</SheetTrigger>
            <SheetContent
                side='right'
                className='max-w-sm md:max-w-md lg:max-w-lg gap-0 h-screen flex flex-col'>
                <SheetHeader className='p-4 border-b'>
                    <SheetTitle className='text-xl font-bold'>Chat</SheetTitle>
                </SheetHeader>
                <div className='flex-1 flex flex-col-reverse overflow-y-auto p-3 border-b'>
                    <div className='flex flex-col-reverse gap-2.5'>
                        {chatState.map((chat, index) => (
                            <div
                                key={index}
                                className={cn(
                                    'text-sm px-2 rounded-lg',
                                    chat.role === 'user'
                                        ? 'bg-primary text-primary-foreground ml-auto max-w-[80%]'
                                        : 'bg-muted max-w-[80%]'
                                )}>
                                <MarkdownViewer
                                    content={chat.message}
                                    streaming={chat.role === 'assistant' && index === 0}
                                />
                            </div>
                        ))}
                    </div>
                </div>
                {loading.chatting && (
                    <p className='flex items-center gap-2 text-sm font-bold animate-pulse m-2'>
                        <Thinker /> Thinking...
                    </p>
                )}
                <div className='mt-auto'>
                    <Chatbox className='p-2' />
                </div>
            </SheetContent>
        </Sheet>
    )
}

export default ChatCanvas
