import { Loader2Icon, LoaderIcon, ScanTextIcon } from 'lucide-react'

import { cn } from '@/lib/utils'

function Spinner({ className, ...props }: React.ComponentProps<'svg'>) {
    return (
        <LoaderIcon
            role='status'
            aria-label='Loading'
            className={cn('size-4 animate-spin', className)}
            {...props}
        />
    )
}

function Loader({ className, ...props }: React.ComponentProps<'svg'>) {
    return (
        <Loader2Icon
            role='status'
            aria-label='Loading'
            className={cn('size-4 animate-spin', className)}
            {...props}
        />
    )
}

function Thinker({ className, ...props }: React.ComponentProps<'svg'>) {
    return (
        <ScanTextIcon
            role='status'
            aria-label='Loading'
            strokeWidth={2}
            className={cn('size-5 animate-pulse', className)}
            {...props}
        />
    )
}

export { Loader, Spinner, Thinker }
