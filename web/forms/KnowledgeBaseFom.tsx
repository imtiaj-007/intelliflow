'use client'

import { zodResolver } from '@hookform/resolvers/zod'
import { Controller, useForm } from 'react-hook-form'
import * as z from 'zod'

import { Button } from '@/components/ui/button'
import { Field, FieldContent, FieldError, FieldLabel } from '@/components/ui/field'
import { Input } from '@/components/ui/input'
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select'
import { Spinner } from '@/components/ui/spinner'
import { useFileActions } from '@/context/AppContext'
import { knowledgeBaseSchema } from '@/forms/schema'
import { embeddingModels } from '@/lib/constants'
import { Eye, EyeOff, File, Upload } from 'lucide-react'
import { useState } from 'react'

export const KnowledgeBaseForm: React.FC = () => {
    const [showApiKey, setShowApiKey] = useState(false)
    const { uploadFile, loading } = useFileActions()

    const form = useForm<z.infer<typeof knowledgeBaseSchema>>({
        resolver: zodResolver(knowledgeBaseSchema),
        defaultValues: {
            embeddingModel: 'text-embedding-3-large',
            apiKey: '',
            file: undefined,
        },
    })

    function handleSubmit(data: z.infer<typeof knowledgeBaseSchema>) {}

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0]
        if (file) {
            form.setValue('file', file)
            uploadFile(file)
        }
    }

    return (
        <form
            id='knowledgebase'
            className='space-y-3'
            onSubmit={form.handleSubmit(handleSubmit)}>
            <Controller
                name='file'
                control={form.control}
                render={({ field, fieldState }) => (
                    <Field
                        orientation='vertical'
                        data-invalid={fieldState.invalid}>
                        <FieldLabel className='text-xs'>File for Knowledge Base</FieldLabel>
                        <FieldContent>
                            <div className='border-2 border-dashed rounded-lg p-4 text-center'>
                                {loading.uploading ? (
                                    <div className='w-full h-full flex items-center justify-center'>
                                        <Spinner />
                                    </div>
                                ) : field.value ? (
                                    <div className='flex flex-col items-center'>
                                        <File className='w-6 h-6 mx-auto text-gray-400 mb-2' />
                                        <span className='text-xs text-gray-600'>
                                            {field.value.name}
                                        </span>
                                    </div>
                                ) : (
                                    <>
                                        <input
                                            type='file'
                                            id='file-upload'
                                            className='hidden'
                                            onChange={handleFileChange}
                                            onBlur={field.onBlur}
                                            ref={field.ref}
                                            name={field.name}
                                        />
                                        <label
                                            htmlFor='file-upload'
                                            className='cursor-pointer'>
                                            <Upload className='w-6 h-6 mx-auto text-gray-400 mb-2' />
                                            <span className='text-sm text-blue-600'>
                                                Upload File
                                            </span>
                                        </label>
                                    </>
                                )}
                            </div>
                        </FieldContent>
                        {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
                    </Field>
                )}
            />

            <Controller
                name='embeddingModel'
                control={form.control}
                render={({ field, fieldState }) => (
                    <Field
                        orientation='vertical'
                        data-invalid={fieldState.invalid}>
                        <FieldLabel className='text-xs'>Embedding Model</FieldLabel>
                        <FieldContent>
                            <Select
                                value={field.value}
                                onValueChange={field.onChange}>
                                <SelectTrigger className='w-full'>
                                    <SelectValue placeholder='Select embedding model' />
                                </SelectTrigger>
                                <SelectContent>
                                    {embeddingModels.map(model => (
                                        <SelectItem
                                            key={model.value}
                                            value={model.value}>
                                            {model.label}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </FieldContent>
                        {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
                    </Field>
                )}
            />

            <Controller
                name='apiKey'
                control={form.control}
                render={({ field, fieldState }) => (
                    <Field
                        orientation='vertical'
                        data-invalid={fieldState.invalid}>
                        <FieldLabel className='text-xs'>API Key</FieldLabel>
                        <FieldContent>
                            <div className='relative'>
                                <Input
                                    type={showApiKey ? 'text' : 'password'}
                                    value={field.value}
                                    onChange={field.onChange}
                                    onBlur={field.onBlur}
                                    placeholder='******************'
                                    className='pr-10'
                                />
                                <Button
                                    variant='ghost'
                                    size='icon'
                                    className='absolute right-0 top-0 h-full'
                                    type='button'
                                    onClick={() => setShowApiKey(!showApiKey)}>
                                    {showApiKey ? (
                                        <EyeOff className='h-4 w-4' />
                                    ) : (
                                        <Eye className='h-4 w-4' />
                                    )}
                                </Button>
                            </div>
                        </FieldContent>
                        {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
                    </Field>
                )}
            />
        </form>
    )
}
