import { CreateWorkflowModal } from '@/components/modals/CreateWorkflow'
import { Button } from '@/components/ui/button'
import { Card, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import type { WorkflowResponse } from '@/services/workflow-service'
import { ExternalLink, Plus } from 'lucide-react'
import Link from 'next/link'

export default async function Home() {
    const workflows: WorkflowResponse[] = []

    return (
        <section
            id='workflow-list'
            className='flex flex-col min-h-100 px-8'>
            <div className='flex items-center justify-between p-4 border-b'>
                <h3>My Stacks</h3>
                <Button>
                    <Plus />
                    New Stack
                </Button>
            </div>
            {workflows?.length ? (
                <div className='grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 p-4'>
                    {workflows.map(workflow => (
                        <Card key={workflow.id}>
                            <CardHeader>
                                <CardTitle>{workflow.name}</CardTitle>
                                <CardDescription className='line-clamp-2'>
                                    {workflow.description}
                                </CardDescription>
                            </CardHeader>
                            <CardFooter className='justify-end'>
                                <Link href={workflow.id}>
                                    <Button
                                        variant='outline'
                                        size='sm'>
                                        <ExternalLink />
                                        Edit Stack
                                    </Button>
                                </Link>
                            </CardFooter>
                        </Card>
                    ))}
                </div>
            ) : (
                <div className='flex-1 flex items-center justify-center'>
                    <Card className='w-sm'>
                        <CardHeader>
                            <CardTitle>Create New Stack</CardTitle>
                            <CardDescription>
                                Start building your generative AI apps with our essential tools and
                                frameworks
                            </CardDescription>
                        </CardHeader>
                        <CardFooter>
                            <CreateWorkflowModal>
                                <Button size='sm'>
                                    <Plus />
                                    New Stack
                                </Button>
                            </CreateWorkflowModal>
                        </CardFooter>
                    </Card>
                </div>
            )}
        </section>
    )
}
