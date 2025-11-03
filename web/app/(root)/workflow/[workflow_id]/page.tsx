import FlowCanvas from '@/components/flow-builder/FlowCanvas'

export default async function Page({ params }: { params: Promise<{ workflow_id: string }> }) {
    const { workflow_id } = await params
    return <FlowCanvas workflowId={workflow_id} />
}
