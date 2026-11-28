import { defineConfig } from 'vite';

export default defineConfig({
  base: './',
  server: {
    host: '0.0.0.0',
    port: 5188,
    strictPort: true,
  },
  preview: {
    host: '0.0.0.0',
    port: 4188,
    strictPort: true,
  },
  build: {
    sourcemap: false,
    chunkSizeWarningLimit: 900,
  },
});
