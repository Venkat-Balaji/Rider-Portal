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

    // Auto-logout when the user closes the tab or browser window.
    // Note: `beforeunload` cannot reliably distinguish between refresh and close.
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      try {
        // Clear local token immediately so reopened tabs won't find it
        localStorage.removeItem('riders:token')
        // Attempt to sign out from Supabase. This is async and may not finish
        // before unload; it's best-effort to invalidate the server session.
        supabase.auth.signOut().catch(() => {
          /* ignore errors */
        })
      } catch (err) {
        // ignore
      }
      // no need to call preventDefault — we don't want to block unload
    }

    window.addEventListener('beforeunload', handleBeforeUnload)

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload)
      sub?.subscription?.unsubscribe?.()
    }
  }, [])
}
