import nextVitals from 'eslint-config-next/core-web-vitals'
import nextTs from 'eslint-config-next/typescript'
import eslintConfigPrettier from 'eslint-config-prettier'
import eslintPluginPrettier from 'eslint-plugin-prettier'
import { defineConfig, globalIgnores } from 'eslint/config'

const eslintConfig = defineConfig([
    ...nextVitals,
    ...nextTs,
    eslintConfigPrettier,
    globalIgnores([
        'node_modules/**',
        '.next/**',
        'out/**',
        'build/**',
        '**/*.d.ts',
        'next-env.d.ts',
    ]),
    {
        plugins: {
            prettier: eslintPluginPrettier,
        },
        rules: {
            'no-console': 'error',
        },
    },
])

export default eslintConfig
