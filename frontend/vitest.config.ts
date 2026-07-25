import { fileURLToPath } from 'node:url'
import { mergeConfig } from 'vite'
import { configDefaults, defineConfig } from 'vitest/config'
import viteConfig from './vite.config'

export default mergeConfig(
  viteConfig,
  defineConfig({
    test: {
      environment: 'happy-dom',
      include: ['src/**/*.test.ts', 'src/**/*.spec.ts'],
      exclude: [...configDefaults.exclude, 'e2e/*'],
      root: fileURLToPath(new URL('./', import.meta.url)),
      css: false,
      globals: true,
      setupFiles: ['./src/__tests__/setup.ts'],
      server: {
        deps: {
          inline: ['vuetify'],
        },
      },
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
      deps: {
        optimizer: {
          web: {
            enabled: true,
          },
        },
      },
    },
  })
)