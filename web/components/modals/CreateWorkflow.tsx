'use client'

import { Button } from '@/components/ui/button'
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from '@/components/ui/dialog'
import { Field, FieldContent, FieldError, FieldLabel } from '@/components/ui/field'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { WorkflowService } from '@/services/workflow-service'
import { zodResolver } from '@hookform/resolvers/zod'
import { useRouter } from 'next/navigation'
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'

const formSchema = z.object({
    title: z.string().min(1, 'Title is required'),
    description: z.string().min(1, 'Description is required'),
})

interface CreateWorkflowModalProps {
    children: React.ReactNode
    onSuccess?: () => void
}

export function CreateWorkflowModal({ children, onSuccess }: CreateWorkflowModalProps) {
    const [open, setOpen] = useState(false)
    const [isLoading, setIsLoading] = useState(false)
    const router = useRouter()

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            title: '',
            description: '',
        },
    })

    async function onSubmit(values: z.infer<typeof formSchema>) {
        setIsLoading(true)
        try {
            const response = await WorkflowService.createWorkflow({
                title: values.title,
                description: values.description,
            })

            if (response.data) {
                setOpen(false)
                form.reset()
                onSuccess?.()
                router.push(`/workflow/${response.data.id}`)
            }
        } catch (error) {
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <Dialog
            open={open}
            onOpenChange={setOpen}>
            <DialogTrigger asChild>{children}</DialogTrigger>
            <DialogContent className='sm:max-w-[425px]'>
                <DialogHeader>
                    <DialogTitle>Create New Workflow</DialogTitle>
                    <DialogDescription>
                        Create a new workflow to start building your AI application.
                    </DialogDescription>
                </DialogHeader>
                <form
                    onSubmit={form.handleSubmit(onSubmit)}
                    className='space-y-4'>
                    <Field
                        orientation='vertical'
                        data-invalid={!!form.formState.errors.title}>
                        <FieldLabel>Title</FieldLabel>
                        <FieldContent>
                            <Input
                                placeholder='Enter workflow title'
                                {...form.register('title')}
                            />
                        </FieldContent>
                        <FieldError>{form.formState.errors.title?.message}</FieldError>
                    </Field>
                    <Field
                        orientation='vertical'
                        data-invalid={!!form.formState.errors.description}>
                        <FieldLabel>Description</FieldLabel>
                        <FieldContent>
                            <Textarea
                                placeholder='Enter workflow description'
                                {...form.register('description')}
                            />
                        </FieldContent>
                        <FieldError>{form.formState.errors.description?.message}</FieldError>
                    </Field>
                    <div className='flex justify-end space-x-2'>
                        <Button
                            type='button'
                            variant='outline'
                            onClick={() => setOpen(false)}
                            disabled={isLoading}>
                            Cancel
                        </Button>
                        <Button
                            type='submit'
                            disabled={isLoading}>
                            {isLoading ? 'Creating...' : 'Create Workflow'}
                        </Button>
                    </div>
                </form>
            </DialogContent>
        </Dialog>
    )
}
