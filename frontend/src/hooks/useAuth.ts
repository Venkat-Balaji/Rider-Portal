import { useEffect } from 'react'
import { supabase } from '@/auth/supabaseClient'
import { useNavigate } from 'react-router-dom'
import create from 'zustand'

type AuthState = {
  token: string | null
  user: any | null
  setSession: (token: string | null, user?: any) => void
  clear: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  user: null,
  setSession: (token, user) => set({ token, user }),
  clear: () => set({ token: null, user: null })
}))

export function useAuth() {
  const setSession = useAuthStore((s) => s.setSession)
  const clear = useAuthStore((s) => s.clear)
  const navigate = useNavigate()

  useEffect(() => {
    supabase.auth.getSession().then((r: any) => {
      const s = r?.data?.session
      if (s?.access_token) {
        setSession(s.access_token, s.user)
        localStorage.setItem('riders:token', s.access_token)
      }
    })

    const { data: sub } = supabase.auth.onAuthStateChange((_event, session) => {
      if (session?.access_token) {
        setSession(session.access_token, session.user)
        localStorage.setItem('riders:token', session.access_token)
      } else {
        clear()
        navigate('/login')
      }
    })

    return () => sub?.subscription?.unsubscribe?.()
  }, [])
}
