'use client'

import { cn } from '@/lib/utils'
import 'highlight.js/styles/github-dark.css'
import { useEffect, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import rehypeHighlight from 'rehype-highlight'
import rehypeRaw from 'rehype-raw'
import remarkBreaks from 'remark-breaks'
import remarkGfm from 'remark-gfm'

interface MarkdownViewerProps {
    content: string
    streaming?: boolean
    className?: string
    maxHeight?: string
}

const MarkdownViewer: React.FC<MarkdownViewerProps> = ({
    content,
    streaming,
    className,
    maxHeight,
}) => {
    const [displayedContent, setDisplayedContent] = useState('')
    const [currentIndex, setCurrentIndex] = useState(0)

    useEffect(() => {
        let timer
        if (!streaming) {
            timer = setTimeout(() => {
                setDisplayedContent(content)
                setCurrentIndex(content.length)
            }, 0)
        }

        timer = setTimeout(() => {
            setDisplayedContent('')
            setCurrentIndex(0)
        }, 0)

        return () => clearTimeout(timer)
    }, [content, streaming])

    useEffect(() => {
        if (!streaming || currentIndex >= content.length) return

        const timer = setTimeout(() => {
            setDisplayedContent(content.slice(0, currentIndex + 1))
            setCurrentIndex(prev => prev + 1)
        }, 10)
        return () => clearTimeout(timer)
    }, [content, currentIndex, streaming])

    return (
        <div
            className={cn('prose dark:prose-invert markdown', className)}
            style={{ maxHeight }}>
            <ReactMarkdown
                remarkPlugins={[remarkGfm, remarkBreaks]}
                rehypePlugins={[rehypeRaw, rehypeHighlight]}>
                {streaming ? displayedContent : content}
            </ReactMarkdown>
        </div>
    )
}

export default MarkdownViewer
