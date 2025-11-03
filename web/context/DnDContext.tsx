'use client'

import { createContext, ReactNode, useContext, useState } from 'react'

type DnDContextType = [string | null, (type: string | null) => void]

const DnDContext = createContext<DnDContextType>([null, () => {}])

interface DnDProviderProps {
    children: ReactNode
}

export const DnDProvider = ({ children }: DnDProviderProps) => {
    const [type, setType] = useState<string | null>(null)

    return <DnDContext.Provider value={[type, setType]}>{children}</DnDContext.Provider>
}

export default DnDContext

export const useDnD = (): DnDContextType => {
    return useContext(DnDContext)
}
