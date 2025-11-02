import Sidebar from '@/components/layout/Sidebar'
import { DnDProvider } from '@/context/DnDContext'

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className='w-full h-full flex'>
            <DnDProvider>
                <Sidebar />
                {children}
            </DnDProvider>
        </div>
    )
}
