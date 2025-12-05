// src/auth/supabaseClient.ts
import { createClient } from '@supabase/supabase-js'

const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL ?? ''
const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY ?? ''

if (!SUPABASE_URL || !SUPABASE_ANON_KEY) {
  // Development-friendly message — throws so you can see the stack trace in dev tools
  throw new Error(
    `Supabase env missing. Please add VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY to your .env (or to process env).
Example:
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key

Current values:
VITE_SUPABASE_URL='${SUPABASE_URL}'
VITE_SUPABASE_ANON_KEY='${SUPABASE_ANON_KEY ? '***present***' : ''}'
`
  )
}

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
  auth: { persistSession: true }
})
