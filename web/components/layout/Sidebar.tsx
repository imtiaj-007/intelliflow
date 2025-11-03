'use client'

import { Button } from '@/components/ui/button'
import { Field, FieldGroup, FieldSet } from '@/components/ui/field'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { EditIcon, SaveIcon } from 'lucide-react'
import { useState } from 'react'
import { NodeOptions } from '../flow-builder/NodeOptions'

interface FormState {
    type: 'input' | 'textarea' | 'select'
    id: string
    name: string
    value: string
    disabled: boolean
}

const Sidebar: React.FC = () => {
    const [formStates, setFormStates] = useState<FormState[]>([
        {
            id: 'workflow-title',
            type: 'input',
            name: 'title',
            value: '',
            disabled: true,
        },
        {
            id: 'workflow-description',
            type: 'textarea',
            name: 'description',
            value: '',
            disabled: true,
        },
    ])

    const handleStateUpdate = (id: string, type: 'visibility' | 'editing', text?: string) => {
        setFormStates(prev =>
            prev.map(state => {
                if (state.id === id) {
                    if (type === 'visibility') {
                        return { ...state, disabled: !state.disabled }
                    } else if (type === 'editing' && text?.trim() !== undefined) {
                        return { ...state, value: text.trim() }
                    }
                }
                return state
            })
        )
    }

    return (
        <aside className='w-64 bg-background flex flex-col gap-2 p-4 border-r'>
            <FieldSet>
                <FieldGroup>
                    {formStates.map(state => {
                        switch (state.type) {
                            case 'input':
                                return (
                                    <Field className='relative'>
                                        <Input
                                            id={state.id}
                                            type='text'
                                            value={state.value}
                                            disabled={state.disabled}
                                            onChange={e =>
                                                handleStateUpdate(
                                                    state.id,
                                                    'editing',
                                                    e.target.value
                                                )
                                            }
                                            placeholder='Chat With AI'
                                            className='pr-8'
                                        />
                                        <div className='absolute inset-0 flex justify-end'>
                                            <Button
                                                size='icon-sm'
                                                variant='ghost'
                                                onClick={() =>
                                                    handleStateUpdate(state.id, 'visibility')
                                                }>
                                                {state.disabled ? <EditIcon /> : <SaveIcon />}
                                            </Button>
                                        </div>
                                    </Field>
                                )
                            case 'textarea':
                                return (
                                    <Field className='relative'>
                                        <Textarea
                                            id={state.id}
                                            rows={4}
                                            value={state.value}
                                            disabled={state.disabled}
                                            onChange={e =>
                                                handleStateUpdate(
                                                    state.id,
                                                    'editing',
                                                    e.target.value
                                                )
                                            }
                                            placeholder='Your feedback helps us improve...'
                                            className='pr-8'
                                        />
                                        <div className='absolute inset-0 flex justify-end'>
                                            <Button
                                                size='icon-sm'
                                                variant='ghost'
                                                onClick={() =>
                                                    handleStateUpdate(state.id, 'visibility')
                                                }>
                                                {state.disabled ? <EditIcon /> : <SaveIcon />}
                                            </Button>
                                        </div>
                                    </Field>
                                )
                            default:
                                return null
                        }
                    })}
                </FieldGroup>
            </FieldSet>
            <NodeOptions />
        </aside>
    )
}

export default Sidebar
