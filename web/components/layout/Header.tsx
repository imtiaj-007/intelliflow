import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import Image from 'next/image'

const Header: React.FC = () => {
    return (
        <header className='flex items-center justify-between px-8 py-4 shadow-sm border-b'>
            <div className='flex items-center gap-2'>
                <Image
                    src='/logo.png'
                    alt='Website Logo'
                    width={32}
                    height={32}
                />
                <h2 className='text-lg md:text-xl font-medium'>IntelliFlow</h2>
            </div>
            <Avatar>
                <AvatarImage
                    src=''
                    alt=''
                />
                <AvatarFallback className='bg-[#B0ACE9] text-white'>IF</AvatarFallback>
            </Avatar>
        </header>
    )
}

export default Header
