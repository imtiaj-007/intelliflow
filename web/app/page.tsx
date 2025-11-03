import { Button } from '@/components/ui/button'
import { Card, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { ExternalLink, Plus } from 'lucide-react'

async function getWorkflows() {
    return Promise.resolve([
        {
            id: '001',
            title: 'Chat With AI',
            description: 'Chat with a smart AI',
        },
        {
            id: '002',
            title: 'Chat With AI',
            description: 'Chat with a smart AI',
        },
        {
            id: '003',
            title: 'Chat With AI',
            description: 'Chat with a smart AI',
        },
        {
            id: '004',
            title: 'Chat With AI',
            description: 'Chat with a smart AI',
        },
    ])
}

export default async function Home() {
    const workflows = await getWorkflows()

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
            {workflows.length ? (
                <div className='grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 p-4'>
                    {workflows.map(workflow => (
                        <Card key={workflow.id}>
                            <CardHeader>
                                <CardTitle>{workflow.title}</CardTitle>
                                <CardDescription className='line-clamp-2'>
                                    {workflow.description}
                                </CardDescription>
                            </CardHeader>
                            <CardFooter className='justify-end'>
                                <Button
                                    variant='outline'
                                    size='sm'>
                                    <ExternalLink />
                                    Edit Stack
                                </Button>
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
                            <Button size='sm'>
                                <Plus />
                                New Stack
                            </Button>
                        </CardFooter>
                    </Card>
                </div>
            )}
        </section>
    )
}
