import * as z from 'zod'

export const knowledgeBaseSchema = z.object({
    embeddingModel: z.string().min(1, 'Embedding model is required.'),
    apiKey: z.string().min(1, 'API key is required.'),
    file: z
        .instanceof(File, { message: 'File is required.' })
        .refine(file => file.size > 0, 'File cannot be empty.')
        .refine(file => file.size <= 2 * 1024 * 1024, 'File size must be less than 2MB.')
        .refine(file => {
            const allowedTypes = [
                'application/pdf',
                'text/plain',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'text/csv',
                'application/json',
            ]
            return allowedTypes.includes(file.type)
        }, 'File type must be PDF, TXT, DOCX, CSV, or JSON.'),
})
