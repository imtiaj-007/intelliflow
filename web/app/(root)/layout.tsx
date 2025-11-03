import Sidebar from '@/components/layout/Sidebar'
import { AppProvider } from '@/context/AppContext'
import { DnDProvider } from '@/context/DnDContext'

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className='w-full h-full flex'>
            <AppProvider>
                <DnDProvider>
                    <Sidebar />
                    {children}
                </DnDProvider>
            </AppProvider>
        </div>
    )
}
