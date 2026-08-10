import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  base: '/signalform-studio/',
  plugins: [react()],
  build: {
    outDir: '../../signalform-studio',
    emptyOutDir: true
  },
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.js']
  }
});
