// src/App.tsx
import React from 'react'
import { QueryClientProvider } from '@tanstack/react-query'
import { queryClient } from './api/reactQueryClient'
import AppRouter from './router'
import { Toaster } from 'react-hot-toast'

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppRouter />
      <Toaster position="top-right" />
    </QueryClientProvider>
  )
}
